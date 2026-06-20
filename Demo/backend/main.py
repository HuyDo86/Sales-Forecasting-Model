from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64

from model_loader import load_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model ExponentialSmoothing đã huấn luyện
model = load_model()

@app.post("/predict")
async def predict_sales(
    file: UploadFile = File(...),
    periods: int = 12
):
    # Đọc CSV
    df = pd.read_csv(io.StringIO((await file.read()).decode("utf-8")))

    # Lấy cột doanh số (LINH HOẠT – KHÔNG LỖI)
    if "Weekly_Sales" in df.columns:
        actual = df["Weekly_Sales"]
    else:
        actual = df.iloc[:, 0]  # lấy cột đầu tiên

    # ===== FORECAST (Exponential Smoothing) =====
    forecast = model.forecast(periods)

    # ===== VẼ BIỂU ĐỒ =====
    plt.figure(figsize=(10, 4))
    plt.plot(actual.values, label="Actual")
    plt.plot(
        range(len(actual), len(actual) + periods),
        forecast.values,
        linestyle="--",
        label="Forecast"
    )
    plt.axvline(len(actual) - 1, color="gray", linestyle=":")
    plt.legend()
    plt.title("Sales Forecast - Exponential Smoothing")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return {
        "model": "Exponential Smoothing (Pretrained)",
        "forecast": [float(x) for x in forecast],
        "image": base64.b64encode(buf.read()).decode("utf-8")
    }
