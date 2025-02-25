import pandas as pd
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def read_root():
    import os
    files = [f for f in os.listdir() if f.endswith(".csv")]
    return {"message": "Football Betting API is running with CSV data!", "available_files": files}

@app.get("/matches/{file_name}")
def get_matches(file_name: str, team: str = Query(None), date: str = Query(None)):
    try:
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(file_name)
        
        # Chọn các cột quan trọng
        columns = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H', 'B365D', 'B365A']
        df = df[columns]

        # Lọc theo đội bóng
        if team:
            df = df[(df["HomeTeam"] == team) | (df["AwayTeam"] == team)]
        
        # Lọc theo ngày
        if date:
            df = df[df["Date"] == date]

        return {"file": file_name, "matches": df.to_dict(orient="records")}
    
    except Exception a
