import os
import asyncio
import uuid
import requests
import chromadb
import numpy as np
import base64
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Path
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity

# FastAPI 앱 생성
app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 환경 변수 로드 ---
SERVER_ROLE = os.getenv('SERVER_ROLE', 'unknown')
AI_SERVER_URL = os.getenv("AI_SERVER_URL")
AI_SERVER_PORT = int(os.getenv("AI_SERVER_PORT", "8001"))
CHROMA_SERVER_HOST = os.getenv("CHROMA_SERVER_HOST", "chromadb")
CHROMA_SERVER_PORT = int(os.getenv("CHROMA_SERVER_PORT", "8000"))

# --- ChromaDB 초기화 ---
client = chromadb.HttpClient(host=CHROMA_SERVER_HOST, port=CHROMA_SERVER_PORT)
collection = client.get_or_create_collection(name="face_embeddings")

# --- AI 서버와 통신하는 헬퍼 함수 ---
async def get_embedding_from_ai_server(image_bytes: bytes):
    if not AI_SERVER_URL:
        raise HTTPException(status_code=500, detail="AI_SERVER_URL이 설정되지 않았습니다.")
    
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    payload = {"image_base64": image_base64}
    
    # requests 호출을 별도의 스레드에서 실행하여 메인 이벤트 루프를 차단하지 않음
    try:
        response = await asyncio.to_thread(
            requests.post,
            f"{AI_SERVER_URL}:{AI_SERVER_PORT}/embedding",
            json=payload,
            timeout=20
        )
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            raise HTTPException(status_code=400, detail=result['error'])
        return result.get("embedding")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"AI 서버에 연결할 수 없습니다: {e}")


VERIFY_THRESHOLD = 0.7

@app.post("/register")
async def register_face(files: list[UploadFile] = File(...), name: str = Form("unknown")):

    if not name or name == "unknown":
        raise HTTPException(status_code=400, detail="사용자 이름을 입력해야 합니다.")
    
    embeddings = []
    for uploaded_file in files:
        image_bytes = await uploaded_file.read()
        try:
            embedding = await get_embedding_from_ai_server(image_bytes)
            embeddings.append(embedding)
        except HTTPException as e:
            # 얼굴 감지 실패 시 해당 파일을 무시하고 계속 진행
            print(f"파일 처리 중 오류 발생: {e.detail}")

    if not embeddings:
        raise HTTPException(status_code=400, detail="제공된 이미지에서 얼굴을 감지하지 못했습니다. 다시 시도해 주세요.")
    
    # 여러 임베딩의 평균을 계산하여 최종 임베딩으로 사용
    avg_embedding = np.mean(embeddings, axis=0)
    
    results = collection.query(
        query_embeddings=[avg_embedding.tolist()],
        n_results=1,
        include=["embeddings"]
    )
    
    if results['ids'] and results['ids'][0]:
        retrieved_id = results['ids'][0][0]
        retrieved_embedding = np.array(results['embeddings'][0][0])
        similarity = cosine_similarity(avg_embedding.reshape(1, -1), retrieved_embedding.reshape(1, -1))[0][0]

        if similarity >= VERIFY_THRESHOLD:
            return JSONResponse(
                status_code=409, 
                content={"message": "이미 등록된 사용자입니다.", "face_id": retrieved_id, "server": SERVER_ROLE, "similarity": round(similarity, 4)}
            )

    try:
        face_id = str(uuid.uuid4())
        
        collection.add(
            embeddings=[avg_embedding.tolist()],
            documents=[f"Face of {name}"],
            metadatas=[{"name": name, "registered_by": SERVER_ROLE}],
            ids=[face_id]
        )
        
        return JSONResponse(
            content={"status": "success", "message": f"얼굴이 등록되었습니다: {name}", "face_id": face_id, "server": SERVER_ROLE}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.post("/verify")
async def verify_face(files: list[UploadFile] = File(...)):
    embeddings = []
    for uploaded_file in files:
        image_bytes = await uploaded_file.read()
        try:
            embedding = await get_embedding_from_ai_server(image_bytes)
            embeddings.append(embedding)
        except HTTPException as e:
            print(f"파일 처리 중 오류 발생: {e.detail}")

    if not embeddings:
        raise HTTPException(status_code=400, detail="제공된 이미지에서 얼굴을 감지하지 못했습니다.")
    
    avg_embedding = np.mean(embeddings, axis=0)

    results = collection.query(
        query_embeddings=[avg_embedding.tolist()],
        n_results=1,
        include=["embeddings", "metadatas"]
    )

    if not results['ids'] or not results['ids'][0]:
        return JSONResponse(status_code=404, content={"message": "등록된 사용자가 없습니다."})

    retrieved_id = results['ids'][0][0]
    retrieved_embedding = np.array(results['embeddings'][0][0]).reshape(1, -1)
    similarity = cosine_similarity(avg_embedding.reshape(1, -1), retrieved_embedding)[0][0]

    retrieved_metadata = results['metadatas'][0][0]  # <-- 2중 리스트 처리
    retrieved_name = retrieved_metadata.get('name')

    if similarity >= VERIFY_THRESHOLD:
        return {"인증": "성공", "ID": retrieved_id, "유사도": round(similarity, 4), "이름": retrieved_name, "server": SERVER_ROLE}
    else:
        return {"인증": "실패", "유사도": round(similarity, 4), "message": "등록된 사용자와 일치하지 않습니다.", "server": SERVER_ROLE}




@app.post("/face/{face_id}/delete")
async def delete_face_with_verification(face_id: str = Path(...), files: list[UploadFile] = File(...)):
    embeddings = []
    for uploaded_file in files:
        image_bytes = await uploaded_file.read()
        try:
            embedding = await get_embedding_from_ai_server(image_bytes)
            embeddings.append(embedding)
        except HTTPException as e:
            print(f"파일 처리 중 오류 발생: {e.detail}")

    if not embeddings:
        raise HTTPException(status_code=400, detail="제공된 이미지에서 얼굴을 감지하지 못했습니다.")
    
    avg_embedding = np.mean(embeddings, axis=0)

    existing_face = collection.get(ids=[face_id], include=["embeddings", "metadatas"])
    if not existing_face['ids']:
        raise HTTPException(status_code=404, detail="삭제할 ID가 존재하지 않습니다.")

    registered_embedding = np.array(existing_face['embeddings'][0][0]).reshape(1, -1)  # 2중 리스트 처리
    similarity = cosine_similarity(avg_embedding.reshape(1, -1), registered_embedding)[0][0]

    if similarity >= VERIFY_THRESHOLD:
        collection.delete(ids=[face_id])
        return {"status": "success", "message": f"ID {face_id} 삭제 완료", "server": SERVER_ROLE}
    else:
        raise HTTPException(status_code=403, detail="업로드한 얼굴이 삭제할 ID와 일치하지 않습니다.")




# 상태 확인용 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "ok", "server": SERVER_ROLE}

@app.get("/db/status")
async def db_status():
    try:
        count = collection.count()
        return {"status": "ok", "total_faces": count, "server": SERVER_ROLE}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@app.get("/db/list")
async def get_face_list():
    try:
        results = collection.get(include=["metadatas", "embeddings", "documents"])
        print("=== /db/list results ===", results)

        faces = []
        ids = results.get("ids", [])
        metadatas = results.get("metadatas", [])
        embeddings = results.get("embeddings", [])
        documents = results.get("documents", [])

        for i, face_id in enumerate(ids):
            metadata = metadatas[i] if i < len(metadatas) else {}
            embedding = embeddings[i] if i < len(embeddings) else []
            document = documents[i] if i < len(documents) else None

            # numpy array → list 변환
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()

            face_info = {
                "id": face_id,
                "metadata": metadata,
                "embedding": embedding,
                "document": document,
            }
            faces.append(face_info)

        return {"faces": faces, "server": SERVER_ROLE}

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("!!! ERROR in /db/list !!!")
        print(error_message)
        return JSONResponse(
            status_code=500,
            content={"message": str(e), "traceback": error_message}
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        ssl_keyfile="/etc/ssl/certs/tls.key", # 시크릿에서 마운트될 경로
        ssl_certfile="/etc/ssl/certs/tls.crt" # 시크릿에서 마운트될 경로
    )

