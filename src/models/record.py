from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Record(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # ObjectId를 문자열로 처리
    userid: str
    type: str
    licensePlate: str
    icon: str
    video: str
    time: datetime
    createdAt: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,  # ObjectId를 문자열로 변환
            datetime: lambda v: v.isoformat(),  # datetime을 ISO 형식으로 변환
        }

class RecordCreate(BaseModel):
    userid: str
    type: str
    licensePlate: str
    icon: str
    video: str
    time: datetime

class RecordUpdate(BaseModel):
    type: Optional[str] = None
    licensePlate: Optional[str] = None
    icon: Optional[str] = None
    video: Optional[str] = None
    time: Optional[datetime] = None
