from typing import Optional, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.events.db.session import AsyncSessionLocal


class AsyncDataStore:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.cache = None

    async def close(self):
        if self.db:
            await self.db.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: Optional[AsyncSessionLocal] = None  # type: ignore
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        if db:
            await db.close()


async def get_data_store(db: AsyncSession = Depends(get_db)) -> AsyncGenerator:
    ds = AsyncDataStore(db=db)
    yield ds
