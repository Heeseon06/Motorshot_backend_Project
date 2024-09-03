from ..models.record import RecordCreate, RecordUpdate, Record
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import HTTPException
from bson import ObjectId

async def get_all_records(db: AsyncIOMotorDatabase):
    records = await db["records"].find().to_list(100)
    # ObjectId를 문자열로 변환
    for record in records:
        record["_id"] = str(record["_id"])
    return [Record(**record) for record in records]

async def create_record(record: RecordCreate, db: AsyncIOMotorDatabase):
    record_data = record.dict()
    result = await db["records"].insert_one(record_data)
    return str(result.inserted_id)

async def get_record(record_id: str, db: AsyncIOMotorDatabase):
    # ObjectId로 변환하여 MongoDB에서 검색
    record = await db["records"].find_one({"_id": ObjectId(record_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    # ObjectId를 문자열로 변환
    record["_id"] = str(record["_id"])
    return Record(**record)

async def get_user_records(user_id: str, db: AsyncIOMotorDatabase):
    records = await db["records"].find({"userid": user_id}).to_list(100)  # "user_id"가 아닌 "userid"로 수정
    # ObjectId를 문자열로 변환
    for record in records:
        record["_id"] = str(record["_id"])
    return [Record(**record) for record in records]

async def update_record(record_id: str, record_update: RecordUpdate, db: AsyncIOMotorDatabase):
    update_data = {k: v for k, v in record_update.dict().items() if v is not None}
    # ObjectId로 변환하여 MongoDB에서 업데이트
    result = await db["records"].update_one({"_id": ObjectId(record_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return await get_record(record_id, db)

async def delete_record(record_id: str, db: AsyncIOMotorDatabase):
    # ObjectId로 변환하여 MongoDB에서 삭제
    result = await db["records"].delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
