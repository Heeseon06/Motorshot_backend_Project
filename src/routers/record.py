from fastapi import APIRouter, Depends, status
from ..controllers import record as recordController
from ..middlewares.user import is_auth
from ..models.record import RecordCreate, RecordUpdate
from ..models.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

# 모든 기록 가져오기
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_records(user=Depends(is_auth), db: AsyncIOMotorDatabase = Depends(get_database)):
    return await recordController.get_all_records(db)

# 새로운 기록 생성
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_record(record: RecordCreate, user=Depends(is_auth), db: AsyncIOMotorDatabase = Depends(get_database)):
    return await recordController.create_record(record, db)

# 특정 기록 가져오기 (ID로)
@router.get("/{record_id}", status_code=status.HTTP_200_OK)
async def get_record_by_id(record_id: str, user=Depends(is_auth), db: AsyncIOMotorDatabase = Depends(get_database)):
    return await recordController.get_record(record_id, db)

# 특정 사용자의 모든 기록 가져오기
@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_records(user_id: str, user=Depends(is_auth), db: AsyncIOMotorDatabase = Depends(get_database)):
    return await recordController.get_user_records(user_id, db)

# 기록 업데이트
@router.put("/{record_id}", status_code=status.HTTP_200_OK)
async def update_record(record_id: str, record_update: RecordUpdate, user=Depends(is_auth), db: AsyncIOMotorDatabase = Depends(get_database)):
    return await recordController.update_record(record_id, record_update, db)

# 기록 삭제
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(id: str, user=Depends(is_auth), db: AsyncIOMotorDatabase = Depends(get_database)):
    await recordController.delete_record(id, db)
    return {"detail": "Record deleted successfully"}
