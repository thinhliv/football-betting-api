import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Football Betting API is running with CSV data!"}

@app.get("/matches")
def get_matches():
    # Đọc file CSV (Thay đổi đường dẫn nếu cần)
    df = pd.read_csv("EPL_2023.csv")

    # Chọn một số cột quan trọng
    data = df[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H', 'B365D', 'B365A']].to_dict(orient="records")

    return {"matches": data}
