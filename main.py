import pandas as pd
from fastapi import FastAPI, Query
import os

app = FastAPI()

@app.get("/")
def read_root():
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
    
    except Exception as e:
        return {"error": str(e)}

# ✅ **NEW FEATURE: Thống kê nâng cao**
@app.get("/stats/{file_name}")
def get_stats(file_name: str):
    try:
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(file_name)

        # Kiểm tra nếu không có dữ liệu
        if df.empty:
            return {"error": "File không có dữ liệu"}

        # Số trận đấu
        total_matches = len(df)

        # Trung bình số bàn thắng
        avg_home_goals = df['FTHG'].mean()
        avg_away_goals = df['FTAG'].mean()

        # Tỷ lệ thắng của đội nhà & đội khách
        home_win_rate = (df['FTHG'] > df['FTAG']).sum() / total_matches
        away_win_rate = (df['FTAG'] > df['FTHG']).sum() / total_matches
        draw_rate = (df['FTHG'] == df['FTAG']).sum() / total_matches

        # Trung bình tỷ lệ cược
        avg_odds_home = df['B365H'].mean()
        avg_odds_draw = df['B365D'].mean()
        avg_odds_away = df['B365A'].mean()

        return {
            "file": file_name,
            "total_matches": total_matches,
            "avg_home_goals": round(avg_home_goals, 2),
            "avg_away_goals": round(avg_away_goals, 2),
            "home_win_rate": round(home_win_rate * 100, 2),
            "away_win_rate": round(away_win_rate * 100, 2),
            "draw_rate": round(draw_rate * 100, 2),
            "avg_odds": {
                "home": round(avg_odds_home, 2),
                "draw": round(avg_odds_draw, 2),
                "away": round(avg_odds_away, 2)
            }
        }
    except Exception as e:
        return {"error": str(e)}
