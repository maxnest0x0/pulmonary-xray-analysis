import uvicorn
from fastapi import FastAPI, UploadFile

from image import process_image

app = FastAPI()

@app.post('/api/analyze')
def analyze(image: UploadFile) -> None:
    im = process_image(image)
    print(im.size)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
