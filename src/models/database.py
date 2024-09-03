from motor.motor_asyncio import AsyncIOMotorClient
from ..config.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.db_uri)
            self.db = self.client[settings.db_name]
            print("데이터베이스 연결 성공")
        except Exception as e:
            print("데이터베이스 연결 실패", e)

    async def close(self):
        self.client.close()
        print("데이터베이스 연결 종료")

mongodb = MongoDB()

async def get_database():
    return mongodb.db
