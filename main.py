import os
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Lấy danh sách file CSV hiện có
CSV_FILES = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".csv")]

@app.get("/")
def read_root():
    return {"message": "Football Betting API is running with CSV data!", "available_files": CSV_FILES}

@app.get("/matches/{file_name}")
def get_matches(file_name: str):
    try:
        # Kiểm tra file có tồn tại không
        if file_name not in CSV_FILES:
            raise HTTPException(status_code=404, detail="CSV file not found!")

        # Đọc file CSV
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        df = pd.read_csv(file_path)

        # Chọn cột cần thiết (nếu cột không có, bỏ qua)
        columns = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'B365H', 'B365D', 'B365A']
        data = df[columns].to_dict(orient="records")

        return {"file": file_name, "matches": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")
