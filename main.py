import pandas as pd
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def read_root():
    import os
    files = [f for f in os.listdir() if f.endswith(".csv")]
    return {"message": "Football Betting API is running with CSV data!", "available_files": files}

@app.get("/matches/{file_name}")
def get_matches(
    file_name: str,
    team: str = Query(None, description="Filter by team name"),
    date: str = Query(None, description="Filter by match date (format: DD/MM/YYYY)"),
    limit: int = Query(None, description="Limit number of matches returned")
):
    try:
        # Đọc file CSV
        df = pd.read_csv(file_name)
        
        # Định dạng lại cột ngày nếu có
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")

        # Lọc theo đội bóng (HomeTeam hoặc AwayTeam)
        if team:
            df = df[(df["HomeTeam"].str.contains(team, case=False, na=False)) | 
                    (df["AwayTeam"].str.contains(team, case=False, na=False))]

        # Lọc theo ngày
        if date:
            df = df[df["Date"] == pd.to_datetime(date, format="%d/%m/%Y", errors="coerce")]

        # Giới hạn số lượng trận trả về
        if limit:
            df = df.head(limit)

        # Chọn một số cột quan trọng
        data = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H', 'B365D', 'B365A']].to_dict(orient="records")

        return {"file": file_name, "matches": data}
    
    except Exception as e:
        return {"error": str(e)}

