# ai_server/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from insightface.app import FaceAnalysis
import numpy as np
import cv2
import base64

app = FastAPI()

class ImagePayload(BaseModel):
    image_base64: str

face_analyzer = FaceAnalysis(name="buffalo_l",  providers=['CPUExecutionProvider'])
face_analyzer.prepare(ctx_id=-1, det_size=(832, 832))

@app.post("/embedding")
async def create_embedding(payload: ImagePayload):
    """Base64로 인코딩된 이미지를 받아 임베딩 벡터를 반환"""
    try:
        image_bytes = base64.b64decode(payload.image_base64)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="유효하지 않은 Base64 이미지 데이터입니다.")

        faces = face_analyzer.get(img)

        if not faces:
            raise HTTPException(status_code=400, detail="이미지에서 얼굴을 감지하지 못했습니다.")

        embedding = faces[0].embedding.tolist()
        
        return {"embedding": embedding}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"AI 서버 오류: {str(e)}"})

@app.get("/health")
def health_check():
    """Healthcheck를 위한 엔드포인트"""
    return {"status": "ok", "server" : "AI_server"}
