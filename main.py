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
        return {"error": "File not found or incorrect format"}

    # Lọc trận đấu của đội
    team_matches = df[(df["HomeTeam"] == team_name) | (df["AwayTeam"] == team_name)]

    # Tính tổng bàn thắng
    total_goals = team_matches.apply(lambda row: row["FTHG"] if row["HomeTeam"] == team_name else row["FTAG"], axis=1).sum()

    return {"team": team_name, "total_goals": int(total_goals)}

@app.get("/stats/{file_name}/record/{team_name}")
def team_record(file_name: str, team_name: str):
    """Thống kê số trận thắng, hòa, thua của một đội"""
    df = load_data(file_name)
    if df is None:
        return {"error": "File not found or incorrect format"}

    # Lọc trận đấu của đội
    team_matches = df[(df["HomeTeam"] == team_name) | (df["AwayTeam"] == team_name)]
    
    wins = 0
    draws = 0
    losses = 0

    for _, row in team_matches.iterrows():
        if row["HomeTeam"] == team_name:
            if row["FTHG"] > row["FTAG"]:
                wins += 1
            elif row["FTHG"] == row["FTAG"]:
                draws += 1
            else:
                losses += 1
        else:
            if row["FTAG"] > row["FTHG"]:
                wins += 1
            elif row["FTHG"] == row["FTAG"]:
                draws += 1
            else:
                losses += 1

    return {"team": team_name, "wins": wins, "draws": draws, "losses": losses}

@app.get("/stats/{file_name}/avg_goals/{team_name}")
def average_goals(file_name: str, team_name: str):
    """Thống kê trung bình bàn thắng của một đội"""
    df = load_data(file_name)
    if df is None:
        return {"error": "File not found or incorrect format"}

    team_matches = df[(df["HomeTeam"] == team_name) | (df["AwayTeam"] == team_name)]
    
    total_matches = len(team_matches)
    total_goals = team_matches.apply(lambda row: row["FTHG"] if row["HomeTeam"] == team_name else row["FTAG"], axis=1).sum()

    avg_goals = total_goals / total_matches if total_matches > 0 else 0

    return {"team": team_name, "average_goals_per_match": round(avg_goals, 2)}

@app.get("/stats/{file_name}/home_vs_away/{team_name}")
def home_vs_away_stats(file_name: str, team_name: str):
    """Thống kê tỷ lệ thắng sân nhà và sân khách"""
    df = load_data(file_name)
    if df is None:
        return {"error": "File not found or incorrect format"}

    home_matches = df[df["HomeTeam"] == team_name]
    away_matches = df[df["AwayTeam"] == team_name]

    home_wins = sum(home_matches["FTHG"] > home_matches["FTAG"])
    away_wins = sum(away_matches["FTAG"] > away_matches["FTHG"])
    
    home_win_rate = home_wins / len(home_matches) if len(home_matches) > 0 else 0
    away_win_rate = away_wins / len(away_matches) if len(away_matches) > 0 else 0

    return {
        "team": team_name,
        "home_win_rate": round(home_win_rate * 100, 2),
        "away_win_rate": round(away_win_rate * 100, 2)
    }
