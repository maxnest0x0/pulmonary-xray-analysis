import time

import uvicorn
from fastapi import FastAPI, UploadFile

from image import process_image, encode_image
from schemas import AnalysisResult, Diagnosis, HeatmapImage, HeatmapPoint

app = FastAPI()

@app.post('/api/analyze')
def analyze(image: UploadFile) -> AnalysisResult:
    start_time = time.time()

    im = process_image(image)
    b64 = encode_image(im)

    return AnalysisResult(
        diagnosis=Diagnosis.NORMAL,
        probabilities={
            Diagnosis.NORMAL: 0.8,
            Diagnosis.VIRAL: 0.15,
            Diagnosis.BACTERIAL: 0.05,
        },
        heatmap_image=HeatmapImage(
            base64=b64,
            mime='image/png',
            dimensions=im.size,
        ),
        heatmap_points=[
            HeatmapPoint(im.size[0] // 2, im.size[1] // 2, 0.9),
        ],
        base_model_name='densenet121-res224-chex',
        dataset_name='',
        processing_time=time.time() - start_time,
        processing_device='cpu',
    )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
