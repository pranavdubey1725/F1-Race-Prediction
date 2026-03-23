from fastapi import APIRouter, HTTPException
from app.schemas import PredictRequest, PredictResponse
from app.model_loader import get_predictor
import numpy as np

router = APIRouter()

# Feature order must match training pipeline
FEATURE_COLUMNS = [
    "driver_id",
    "constructor_id",
    "circuit_id",
    "grid_position",
    "qualifying_time_ms",
    "avg_pit_stop_ms",
    "driver_wins",
    "driver_points",
    "constructor_wins",
    "constructor_points",
    "round_number",
    "year",
]


def confidence_label(position: int) -> str:
    if position <= 3:
        return "Podium Finish 🏆"
    elif position <= 6:
        return "Points Finish ✅"
    elif position <= 10:
        return "Top 10 Finish"
    elif position <= 15:
        return "Midfield Finish"
    else:
        return "Backmarker Finish"


@router.post("/", response_model=PredictResponse, summary="Predict race finishing position")
def predict_position(data: PredictRequest):
    """
    Given driver, constructor, circuit, and race context features,
    predict the expected finishing position (1–20).
    """
    try:
        predictor = get_predictor("f1_model")

        feature_values = [
            data.driver_id,
            data.constructor_id,
            data.circuit_id,
            data.grid_position,
            data.qualifying_time_ms if data.qualifying_time_ms is not None else 85000.0,
            data.avg_pit_stop_ms if data.avg_pit_stop_ms is not None else 25000.0,
            data.driver_wins,
            data.driver_points,
            data.constructor_wins,
            data.constructor_points,
            data.round_number,
            data.year,
        ]

        X = np.array([feature_values], dtype=float)
        raw_pred = predictor.predict(X)
        position = int(np.clip(round(float(raw_pred[0])), 1, 20))

        return PredictResponse(
            predicted_position=position,
            confidence_label=confidence_label(position),
            model_used="f1_model.joblib" if not hasattr(predictor, "__class__") or predictor.__class__.__name__ != "MockPredictor" else "mock_predictor",
            input_summary={
                "grid_position": data.grid_position,
                "driver_wins": data.driver_wins,
                "constructor_wins": data.constructor_wins,
                "round_number": data.round_number,
                "year": data.year,
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/batch", summary="Batch predict for multiple drivers")
def predict_batch(drivers: list[PredictRequest]):
    """Predict positions for a list of drivers in one race."""
    if len(drivers) > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 drivers per batch.")

    results = []
    for d in drivers:
        result = predict_position(d)
        results.append({
            "driver_id": d.driver_id,
            "grid_position": d.grid_position,
            "predicted_position": result.predicted_position,
            "confidence_label": result.confidence_label,
        })

    # Sort by predicted finishing position
    results.sort(key=lambda x: x["predicted_position"])
    return {"predictions": results, "total_drivers": len(results)}