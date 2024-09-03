from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # 기본값 None으로 설정하고 문자열로 저장
    name: str  # 필수 필드
    userid: str  # 필수 필드
    hp: str  # 필수 필드
    email: str  # 필수 필드

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}  # ObjectId를 문자열로 인코딩

class UserCreate(UserBase):
    password: str  # 필수 필드

class UserLogin(BaseModel):
    userid: str  # 필수 필드
    password: str  # 필수 필드

class UserInDB(UserBase):
    hashed_password: str  # 데이터베이스에 저장된 암호화된 비밀번호

async def find_by_id(db, id: str) -> Optional[UserInDB]:
    user = await db["users"].find_one({"_id": ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])  # ObjectId를 문자열로 변환
        return UserInDB(**user)
    return None

async def find_by_userid(db, userid: str) -> Optional[UserInDB]:
    user = await db["users"].find_one({"userid": userid})
    if user:
        user['_id'] = str(user['_id'])  # ObjectId를 문자열로 변환
        return UserInDB(**user)
    return None

async def create_user(db, user: UserCreate) -> str:
    user_data = user.dict(by_alias=True, exclude_unset=True)  # 기본값이 None인 필드를 제외하고 변환
    result = await db["users"].insert_one(user_data)
    return str(result.inserted_id)

async def delete_user(db, userid: str) -> bool:
    result = await db["users"].delete_one({"userid": userid})
    return result.deleted_count == 1
