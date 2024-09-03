from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException
from ..models.user import UserCreate, UserLogin, UserInDB, find_by_userid, create_user, delete_user
from ..config.config import settings
from ..models.database import get_database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def signup(user: UserCreate):
    db = await get_database()
    existing_user = await find_by_userid(db, user.userid)
    if existing_user:
        raise HTTPException(status_code=409, detail=f"{user.userid}이 이미 존재합니다.")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = UserInDB(**user.dict(), hashed_password=hashed_password)
    user_id = await create_user(db, new_user)
    return {"id": user_id, "message": "회원가입 성공"}

async def login(user: UserLogin):
    db = await get_database()
    db_user = await find_by_userid(db, user.userid)
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못되었습니다.")
    
    token = jwt.encode({"id": str(db_user.id)}, settings.jwt_secret_key, algorithm="HS256")
    return {"token": token}

async def del_user(userid: str):
    db = await get_database()
    success = await delete_user(db, userid)
    if not success:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"message": "사용자 삭제 완료"}

async def me(userid: str):
    db = await get_database()
    user = await find_by_userid(db, userid)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user
