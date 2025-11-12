import pytest
from pydantic import ValidationError
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas import Diagnosis, HeatmapImage, HeatmapPoint, AnalysisResult


class TestDiagnosis:
  def test_diagnosis_values(self):
    assert Diagnosis.NORMAL == 'normal'
    assert Diagnosis.VIRAL == 'viral_pneumonia'
    assert Diagnosis.BACTERIAL == 'bacterial_pneumonia'


class TestHeatmapImage:
  def test_valid_heatmap_image(self):
    valid_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    heatmap = HeatmapImage(
      base64=valid_base64,
      mime="image/png",
      dimensions=(100, 100)
    )

    assert heatmap.base64 == valid_base64
    assert heatmap.mime == "image/png"


class TestAnalysisResult:
  def test_valid_analysis_result(self):
    valid_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    heatmap_image = HeatmapImage(
      base64=valid_base64,
      mime="image/png",
      dimensions=(100, 100)
    )

    result = AnalysisResult(
      diagnosis=Diagnosis.NORMAL,
      probabilities={
        Diagnosis.NORMAL: 0.7,
        Diagnosis.VIRAL: 0.2,
        Diagnosis.BACTERIAL: 0.1
      },
      heatmap_image=heatmap_image,
      heatmap_points=[
        HeatmapPoint(x=10, y=20, intensity=0.8),
      ],
      base_model_name="densenet121-res224-chex",
      dataset_name="chest_xray",
      processing_time=2.5,
      processing_device="cpu"
    )

    assert result.diagnosis == Diagnosis.NORMAL
