from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import predict, stats
import os

app = FastAPI(
    title="F1 Race Position Predictor API",
    description="Predict Formula 1 race finishing positions using historical data and ML models.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(stats.router, prefix="/api/stats", tags=["EDA & Statistics"])

# Serve frontend static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def serve_frontend():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "F1 Race Position Predictor API is running. Visit /docs for API documentation."}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "F1 Race Predictor"}