from fastapi import APIRouter
from .user import router as user_router
from .record import router as record_router

router = APIRouter()

# 사용자 관련 라우터 추가
router.include_router(user_router, prefix="/user")

# 기록 관련 라우터 추가
router.include_router(record_router, prefix="/record")
