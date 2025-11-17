import time

import uvicorn
from fastapi import FastAPI, UploadFile

from image import process_image, prepare_image, encode_image
from heatmap import make_example_heatmap, apply_threshold, render_heatmap, dense_to_sparse
from schemas import AnalysisResult, Diagnosis, HeatmapImage

app = FastAPI()

@app.post('/api/analyze')
def analyze(image: UploadFile) -> AnalysisResult:
    start_time = time.time()

    im = process_image(image)
    heatmap = apply_threshold(make_example_heatmap(im.width, im.height, im.width / 2, im.height / 2, min(im.size) / 10))
    b64 = encode_image(render_heatmap(prepare_image(im), heatmap))
    points = dense_to_sparse(heatmap)

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
        heatmap_points=points,
        base_model_name='densenet121-res224-chex',
        dataset_name='',
        processing_time=time.time() - start_time,
        processing_device='cpu',
    )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
