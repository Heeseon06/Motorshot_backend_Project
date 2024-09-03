from fastapi import APIRouter, Depends, HTTPException, status
from ..controllers import user as authController
from ..middlewares.user import is_auth
from ..models.user import UserCreate, UserLogin, UserBase

router = APIRouter()

# 회원 탈퇴
@router.delete("/{userid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(userid: str, user=Depends(is_auth)):
    return await authController.del_user(userid)

# 회원 가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    return await authController.signup(user)

# 로그인
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    return await authController.login(user)

# 사용자 정보 가져오기
@router.post("/get_user", status_code=status.HTTP_200_OK)
async def get_user(user: UserBase):
    return await authController.me(user.userid)

# 토큰 검증
@router.get("/verifyToken", status_code=status.HTTP_200_OK)
async def verify_token(user=Depends(is_auth)):
    token = user['token']
    return {"success": True, "user": user, "token": token}
