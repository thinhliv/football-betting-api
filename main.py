import pandas as pd
from fastapi import FastAPI, Query
import os

app = FastAPI()

@app.get("/")
def read_root():
    files = [f for f in os.listdir() if f.endswith(".csv")]
    return {"message": "Football Betting API is running with CSV data!", "available_files": files}

def load_data(file_name):
    """Hàm load dữ liệu từ file CSV"""
    try:
        df = pd.read_csv(file_name)
        df = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]  # Chỉ giữ cột quan trọng
        return df
    except Exception as e:
        return None

@app.get("/stats/{file_name}/team/{team_name}")
def team_stats(file_name: str, team_name: str):
    """Thống kê tổng số bàn thắng của một đội"""
    df = load_data(file_name)
    if df is None:
        return {"error": "File not foun
