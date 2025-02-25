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

# ✅ Thêm Endpoint Mới: Thống kê dữ liệu
@app.get("/stats/{file_name}")
def get_stats(file_name: str, team: str = Query(None)):
    try:
        df = pd.read_csv(file_name)

        # Chọn các cột quan trọng
        columns = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']
        df = df[columns]

        # Tổng số trận đấu của đội bóng
        if team:
            team_df = df[(df["HomeTeam"] == team) | (df["AwayTeam"] == team)]
        else:
            team_df = df

        total_matches = len(team_df)

        # Tổng số bàn thắng của đội bóng
        total_goals = team_df["FTHG"].sum() + team_df["FTAG"].sum()
        avg_goals_per_match = total_goals / total_matches if total_matches > 0 else 0

        # Tính tỷ lệ thắng/thua/hòa của đội bóng
        if team:
            wins = team_df[(team_df["HomeTeam"] == team) & (team_df["FTHG"] > team_df["FTAG"])].shape[0] + \
                   team_df[(team_df["AwayTeam"] == team) & (team_df["FTAG"] > team_df["FTHG"])].shape[0]

            draws = team_df[team_df["FTHG"] == team_df["FTAG"]].shape[0]

            losses = total_matches - (wins + draws)

            win_rate = wins / total_matches if total_matches > 0 else 0
            draw_rate = draws / total_matches if total_matches > 0 else 0
            loss_rate = losses / total_matches if total_matches > 0 else 0
        else:
            win_rate, draw_rate, loss_rate = None, None, None

        return {
            "file": file_name,
            "team": team if team else "All Teams",
            "total_matches": total_matches,
            "total_goals": total_goals,
            "avg_goals_per_match": round(avg_goals_per_match, 2),
            "win_rate": round(win_rate, 2) if win_rate is not None else None,
            "draw_rate": round(draw_rate, 2) if draw_rate is not None else None,
            "loss_rate": round(loss_rate, 2) if loss_rate is not None else None,
        }

    except Exception as e:
        return {"error": str(e)}
