import uvicorn
from fastapi import FastAPI
from core.engine import AsyncMLEngine, InferenceRequest, InferenceResult
import time
import uuid

app = FastAPI(title="ScaleStream-ML-Pipeline Gateway")
engine = AsyncMLEngine()

@app.get("/health")
def health_check():
    return {"status": "online", "model": engine.model_name}

@app.post("/v1/predict", response_model=InferenceResult)
async def predict(data: dict):
    \"\"\"
    Main inference endpoint. Demonstrates async request handling.
    \"\"\"
    request_id = str(uuid.uuid4())
    req = InferenceRequest(
        request_id=request_id,
        input_data=data,
        timestamp=time.time()
    )
    
    result = await engine.enqueue_and_wait(req)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)