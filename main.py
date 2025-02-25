import os
import pandas as pd
from fastapi import FastAPI, Query

app = FastAPI()

# Lấy danh sách file CSV trong thư mục
csv_files = [f for f in os.listdir() if f.endswith(".csv")]

@app.get("/")
def read_root():
    return {"message": "Football Betting API is running with CSV data!", "available_files": csv_files}

@app.get("/matches/{file_name}")
def get_matches(
    file_name: str,
    date: str = Query(None, description="Lọc theo ngày (định dạng dd/mm/yyyy)"),
    home_team: str = Query(None, description="Lọc theo đội chủ nhà"),
    away_team: str = Query(None, description="Lọc theo đội khách")
):
    """
    API lấy dữ liệu trận đấu từ file CSV với các bộ lọc theo ngày, đội chủ nhà và đội khách.
    """

    # Kiểm tra file có tồn tại không
    if file_name not in csv_files:
        return {"error": "File not found!"}

    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(file_name)

    # Chỉ giữ lại các cột quan trọng
    columns_to_keep = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H', 'B365D', 'B365A']
    df = df[columns_to_keep]

    # Lọc theo ngày
    if date:
        df = df[df['Date'] == date]

    # Lọc theo đội chủ nhà
    if home_team:
        df = df[df['HomeTeam'].str.contains(home_team, case=False, na=False)]

    # Lọc theo đội khách
    if away_team:
        df = df[df['AwayTeam'].str.contains(away_team, case=False, na=False)]

    # Trả về dữ liệu dạng JSON
    return {"file": file_name, "matches": df.to_dict(orient="records")}
