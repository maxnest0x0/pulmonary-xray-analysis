from typing import Annotated, NamedTuple
from enum import StrEnum

from pydantic import BaseModel, Field

NormFloat = Annotated[float, Field(ge=0.0, le=1.0)]

class Diagnosis(StrEnum):
    NORMAL = 'normal'
    VIRAL = 'viral_pneumonia'
    BACTERIAL = 'bacterial_pneumonia'

class HeatmapImage(BaseModel):
    base64: str
    mime: str
    dimensions: tuple[int, int]

class HeatmapPoint(NamedTuple):
    x: int
    y: int
    intensity: NormFloat

class AnalysisResult(BaseModel):
    diagnosis: Diagnosis
    probabilities: dict[Diagnosis, NormFloat]
    heatmap_image: HeatmapImage | None
    heatmap_points: list[HeatmapPoint] | None
    base_model_name: str
    processing_time: float
    processing_device: str
