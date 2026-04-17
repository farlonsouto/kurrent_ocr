import time

from fastapi import FastAPI, UploadFile, File, HTTPException

from src.core.inference import KurrentInference
from src.core.segmenter import segment_lines

app = FastAPI(title="Kurrentschrift OCR API")

# Initialize model on startup
ocr_engine = KurrentInference()


@app.post("/v1/transcribe")
async def transcribe_page(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    start_time = time.time()

    # Read image
    image_bytes = await file.read()

    # 1. Segment page into lines
    try:
        line_strips = segment_lines(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentation failed: {str(e)}")

    if not line_strips:
        return {"text": "", "lines_processed": 0, "status": "No text detected"}

    # 2. Run Inference (One page at a time, but lines are batched)
    try:
        results = ocr_engine.predict(line_strips)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model inference failed: {str(e)}")

    full_text = "\n".join(results)

    return {
        "text": full_text,
        "lines_processed": len(results),
        "processing_time_sec": round(time.time() - start_time, 2),
        "model": "dh-unibe/trocr-kurrent-XVI-XVII"
    }


@app.get("/health")
def health_check():
    return {"status": "ready", "device": str(ocr_engine.device)}
