from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from ..models.user import find_by_id
from ..config.config import settings
from ..models.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

AUTH_ERROR = {"message": "인증 오류"}

security = HTTPBearer()

async def is_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> dict:
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="토큰이 제공되지 않았습니다.")
    
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail=AUTH_ERROR)
        
        user = await find_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail=AUTH_ERROR)
        
        return {"user": user, "token": token}
    
    except JWTError as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
