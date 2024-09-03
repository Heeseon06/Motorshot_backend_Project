import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from src.routers import user, record
from src.config.config import settings
from src.models.database import mongodb
from src.models.helmet_detection import detect_helmets_in_frame, load_model
from starlette.responses import JSONResponse
import cv2
import numpy as np
import tempfile
import os
import logging
import base64
import asyncio
import json

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket 연결을 저장할 세트
active_connections = set()

# 모델 로드
model = load_model()

# MongoDB 연결
@app.on_event("startup")
async def startup_db_client():
    await mongodb.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await mongodb.close()

# 라우터 추가
app.include_router(user.router, prefix="/user")
app.include_router(record.router, prefix="/record")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # 클라이언트로부터 메시지를 기다립니다.
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        active_connections.remove(websocket)

async def broadcast_log(message: str):
    disconnected = set()
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except WebSocketDisconnect:
            disconnected.add(connection)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {str(e)}")
            disconnected.add(connection)
    
    active_connections.difference_update(disconnected)
    for conn in disconnected:
        logger.info("Removed closed WebSocket connection")

async def send_frame_to_websockets(frame_data: dict):
    disconnected = set()
    for connection in active_connections:
        try:
            await connection.send_json(frame_data)
        except WebSocketDisconnect:
            disconnected.add(connection)
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {str(e)}")
            disconnected.add(connection)
    
    active_connections.difference_update(disconnected)
    for conn in disconnected:
        logger.info("Removed closed WebSocket connection")

async def process_video_file(file: UploadFile):
    try:
        # 임시 파일 생성
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_filename = temp_file.name
            temp_file.write(await file.read())
        
        cap = cv2.VideoCapture(temp_filename)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Cannot open video file")

        frame_count = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = 1 / fps  # 초 단위
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # frame = cv2.resize(frame, (640, 480))
            frame_count += 1
            if frame_count % 20 != 0:  # 매 10프레임마다 처리
                continue
            
            detections = detect_helmets_in_frame(model, frame)  # 모델과 함께 frame 전달
            
            # 바운딩 박스 그리기
            for det in detections:
                x1, y1, x2, y2 = map(int, det['bbox'])
                color = (0, 255, 0) if det['class'] == 1 else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # 프레임을 base64로 인코딩
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # 프레임 데이터 생성
            frame_data = {
                "frame": frame_count,
                "detections": detections,
                "frame_data": frame_base64
            }

            # 프레임 데이터를 WebSocket을 통해 전송
            await send_frame_to_websockets(frame_data)
            await asyncio.sleep(0.1)  # 약간의 대기 시간

            log_message = f"Processed frame {frame_count}/{total_frames}"
            logger.info(log_message)
            await broadcast_log(log_message)

        cap.release()
        log_message = f"Video processing completed: {file.filename}"
        logger.info(log_message)
        await broadcast_log(log_message)

    except Exception as e:
        error_message = f"Error processing video: {str(e)}"
        logger.error(error_message)
        await broadcast_log(error_message)
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # 자원 정리
        if cap.isOpened():
            cap.release()
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {e}")

@app.post("/detect_helmet_video")
async def detect_helmet_video_endpoint(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    log_message = f"Processing video: {file.filename}"
    logger.info(log_message)
    await broadcast_log(log_message)
    
    try:
        # 비디오 파일을 처리하고 프레임을 WebSocket을 통해 전송
        await process_video_file(file)
        return {"detail": "Video processing completed"}
    
    except HTTPException as e:
        raise e  # HTTPException은 여기서 그대로 전파
    
    except Exception as e:
        error_message = f"Error processing video: {str(e)}"
        logger.error(error_message)
        await broadcast_log(error_message)
        raise HTTPException(status_code=500, detail=str(e))

# 에러 처리 미들웨어
@app.middleware("http")
async def catch_exceptions_middleware(request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        error_message = f"Unhandled exception: {str(e)}"
        logger.error(error_message)
        await broadcast_log(error_message)
        return JSONResponse(status_code=500, content={"detail": str(e)})

# 서버 실행
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(settings.host_port))
