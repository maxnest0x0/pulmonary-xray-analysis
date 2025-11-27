import time

import uvicorn
from fastapi import FastAPI, UploadFile

from image import process_image, prepare_image, encode_image
from heatmap import make_example_heatmap, apply_threshold, render_heatmap, dense_to_sparse
from schemas import AnalysisResult, Diagnosis, HeatmapImage
# torchxrayvision imports 'model' module internally, so we have no choice but to rename our module
from model_.arch_model import prepare_model_for_viz_and_predict, run_model_with_features, DEVICE

app = FastAPI()
model, hooks = prepare_model_for_viz_and_predict('model_/best_model.pth')

@app.post('/api/analyze')
def analyze(image: UploadFile) -> AnalysisResult:
    start_time = time.time()

    im = process_image(image)
    img = prepare_image(im)
    pred, probs, cam = run_model_with_features(img, model, hooks)
    if cam is not None:
        heatmap = apply_threshold(cam)
        b64 = encode_image(render_heatmap(img, heatmap))
        viz = HeatmapImage(
            base64=b64,
            mime='image/png',
            dimensions=im.size,
        )
        points = dense_to_sparse(heatmap)
    else:
        viz = None
        points = None

    return AnalysisResult(
        diagnosis=pred,
        probabilities=probs,
        heatmap_image=viz,
        heatmap_points=points,
        base_model_name=model.weights,
        processing_time=time.time() - start_time,
        processing_device=DEVICE.type,
    )

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
