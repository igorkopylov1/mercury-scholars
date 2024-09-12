import logging
import threading
import typing as tp
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.dialects import postgresql

from .schema import Employees, Chat_info
from ..libs import ttl_cache


import asyncio
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PGClient:
    def __init__(self, pg_url: str) -> None:
        super().__init__()
        self._pg_url = pg_url
        self._thread_safe_storage = threading.local()
        self._insert_operation_info_lock = threading.RLock()

    @property
    def _engine(self) -> AsyncEngine:
        if getattr(self._thread_safe_storage, "engine", None) is None:
            self._thread_safe_storage.engine = create_async_engine(
                self._pg_url, connect_args={"statement_cache_size": 0}
            )
        return self._thread_safe_storage.engine
    
    @ttl_cache(maxsize=50, ttl=5 * 60)
    async def get_employees(
        self,
        id: tp.Optional[int] = None,
        name: tp.Optional[str] = None,
        position: tp.Optional[str] = None,
    ) -> list[Employees]:
        query = self._select(Employees)

        if id is not None:
            query = query.where(Employees.id == id)
        if name is not None:
            query = query.where(Employees.name == name)
        if position is not None:
            query = query.where(Employees.position == position)

        return await self._fetch(query)

    @ttl_cache(maxsize=50, ttl=10 * 60)
    async def get_chat_info(
        self,
        chat_id: tp.Optional[str] = None,
        first_name: tp.Optional[str] = None,
        start_date: tp.Optional[str] = None,
        end_date: tp.Optional[str] = None,
        pay: tp.Optional[int] = None,
    ) -> list[Chat_info]:
        query = self._select(Chat_info)

        if chat_id is not None:
            query = query.where(Chat_info.chat_id == chat_id)
        if first_name is not None:
            query = query.where(Chat_info.first_name == first_name)

        if start_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.where(Chat_info.start_date >= start_date)
        if end_date is not None:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.where(Chat_info.end_date <= end_date)
        if pay is not None:
            query = query.where(Chat_info.pay >= pay)

        return await self._fetch(query)
    
    async def upsert_chat_info(
        self,
        users: list[dict],
    ) -> None:
        if not users:
            return
        
        logger.debug("Upserting Users...")

        insert_stmt = postgresql.insert(Chat_info).values(users)
        primary_keys = [column.name for column in Chat_info.__table__.primary_key]
        update_set = {col.name: col for col in insert_stmt.excluded if col.name not in primary_keys}
        do_update_stmt = insert_stmt.on_conflict_do_update(
            index_elements=primary_keys,
            set_=update_set
        )
        return await self._execute_insert(do_update_stmt)
    
    async def _fetch(self, query: sa.sql.Select):
        objects = [obj for obj, in (await self._execute_select(query))]#.unique()]
        logger.debug(f"Fetched {len(objects)} items.")
        return objects

    async def _execute_insert(
        self,
        stmt: sa.sql.Insert,
    ) -> sa.engine.Result: # TODO: add return type
        async with AsyncSession(self._engine) as session:
            async with session.begin():
                stmt_result = await session.execute(stmt)
            return stmt_result.inserted_primary_key

    async def _execute_select(
        self,
        stmt: (
            sa.sql.Select | sa.sql.Insert
        ),
        *,
        execution_options: dict = {},
    ) -> sa.engine.Result:
        async with AsyncSession(self._engine) as session:
            stmt_result = await session.execute(stmt, execution_options=execution_options)
            return stmt_result
    
    @staticmethod
    def _select(*args, **kwargs) -> sa.sql.Select:
        return sa.select(*args, **kwargs)


# chat_id: Mapped[str] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
# first_name: Mapped[str] = mapped_column(sa.String(100))
# start_date: Mapped[sa.Date] = mapped_column(sa.Date)
# end_date: Mapped[sa.Date] = mapped_column(sa.Date)
# pay: Mapped[int] = mapped_column(sa.Integer)
# async def main():
#     DB_USERNAME=os.environ.get("DB_USERNAME", "Gosha Kucenko")
#     DB_PASSWORD=os.environ.get("DB_PASSWORD", "huckme")
#     DB_HOSTNAME=os.environ.get("DB_HOSTNAME", "localhost")
#     DB_PORT=os.environ.get("DB_PORT", "port")
#     DB_DATABASE=os.environ.get("DB_DATABASE", "db_dev")
#     DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
#     print(DATABASE_URL)
#     pg_client = PGClient(DATABASE_URL)
#     user = dict(
#         chat_id="1292456766",
#         first_name="Igor",
#         start_date=datetime.strptime("2024-09-03", "%Y-%m-%d").date(),
#         end_date=datetime.strptime("2025-10-03", "%Y-%m-%d").date(),
#         pay=0
#     )

#     print(await pg_client.upsert_chat_info(user))

# if __name__ == "__main__":
#     asyncio.run(main())