from pydantic import BaseModel, Field
from typing import Optional, List


class PredictRequest(BaseModel):
    """Input features for race position prediction."""

    driver_id: int = Field(..., description="Encoded driver ID", example=1)
    constructor_id: int = Field(..., description="Encoded constructor/team ID", example=3)
    circuit_id: int = Field(..., description="Encoded circuit ID", example=11)
    grid_position: int = Field(..., ge=1, le=20, description="Starting grid position", example=3)
    qualifying_time_ms: Optional[float] = Field(None, description="Qualifying lap time in milliseconds", example=82500.0)
    avg_pit_stop_ms: Optional[float] = Field(None, description="Average pit stop duration in ms", example=25000.0)
    driver_wins: int = Field(0, ge=0, description="Driver's total wins up to this race", example=5)
    driver_points: float = Field(0.0, ge=0, description="Driver's cumulative points this season", example=120.5)
    constructor_wins: int = Field(0, ge=0, description="Constructor's total wins", example=8)
    constructor_points: float = Field(0.0, ge=0, description="Constructor's points this season", example=250.0)
    round_number: int = Field(..., ge=1, le=25, description="Race round number in the season", example=7)
    year: int = Field(..., ge=1950, le=2024, description="Season year", example=2023)


class DriverPrediction(BaseModel):
    driver_id: int
    predicted_position: int
    confidence_label: str


class PredictResponse(BaseModel):
    predicted_position: int
    confidence_label: str
    model_used: str
    input_summary: dict


class DriverStats(BaseModel):
    driver_id: int
    driver_name: str
    total_wins: int
    total_podiums: int
    avg_finish_position: float
    races_entered: int
    best_finish: int


class CircuitStats(BaseModel):
    circuit_id: int
    circuit_name: str
    country: str
    avg_winner_grid: float
    total_races: int


class ConstructorStats(BaseModel):
    constructor_id: int
    constructor_name: str
    total_wins: int
    avg_finish_position: float


class SeasonSummary(BaseModel):
    year: int
    total_races: int
    unique_winners: int
    dominant_constructor: str


class StatsOverview(BaseModel):
    total_races: int
    total_drivers: int
    total_circuits: int
    years_covered: List[int]
    top_drivers: List[DriverStats]
    top_constructors: List[ConstructorStats]