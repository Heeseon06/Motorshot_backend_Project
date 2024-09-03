from ultralytics import YOLO
import torch
import os
import cv2
import numpy as np
from fastapi import HTTPException

def load_model(weights_path='helmet_yolo.pt'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, weights_path)
    
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Model file not found: {full_path}")
    
    model = YOLO(full_path)
    return model

def detect_helmet(model, image, conf_thres=0.25, iou_thres=0.45):
    results = model(image, conf=conf_thres, iou=iou_thres)
    return results[0]  # 첫 번째 (그리고 유일한) 이미지의 결과를 반환

def process_detections(results):
    detections = []
    if results.boxes is not None:
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = box.conf.item()
            class_id = int(box.cls.item())
            detections.append({
                'bbox': [int(x1), int(y1), int(x2), int(y2)],
                'confidence': float(confidence),
                'class': class_id
            })
    return detections

def detect_helmets_in_frame(model, frame, conf_thres=0.25, iou_thres=0.45):
    results = detect_helmet(model, frame, conf_thres=conf_thres, iou_thres=iou_thres)
    
    # 헬멧 클래스만 필터링 (클래스 인덱스는 모델에 따라 다를 수 있음)
    helmet_class_indices = [0, 1]  # 예: 0은 no_helmet, 1은 helmet
    
    detections = []
    if results.boxes is not None:
        for box in results.boxes:
            if int(box.cls) in helmet_class_indices:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = float(box.conf)
                cls = int(box.cls)
                detections.append({
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': conf,
                    'class': cls
                })
    
    return detections

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_results = []
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 프레임 단위로 헬멧 감지 수행
            results = detect_helmets_in_frame(model, frame)
            frame_results.append(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
    finally:
        cap.release()  # 캡처 객체 해제
        cv2.destroyAllWindows()  # 모든 OpenCV 윈도우 닫기

    return frame_results

# 글로벌 변수로 모델 로드
try:
    model = load_model()
    print(f"Model loaded successfully: {model}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
