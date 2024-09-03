import logging
import threading
import typing as tp
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from datetime import datetime


from .schema import Employees, Users
from ..libs import ttl_cache


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
    async def get_users(
        self,
        chat_id: tp.Optional[str] = None,
        first_name: tp.Optional[str] = None,
        start_date: tp.Optional[str] = None,
        end_date: tp.Optional[str] = None,
        pay: tp.Optional[int] = None,
    ) -> list[Users]:
        query = self._select(Users)

        if chat_id is not None:
            query = query.where(Users.chat_id == chat_id)
        if first_name is not None:
            query = query.where(Users.first_name == first_name)

        if start_date is not None:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.where(Users.start_date >= start_date)
        if end_date is not None:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.where(Users.end_date <= end_date)
        if pay is not None:
            query = query.where(Users.pay >= pay)

        return await self._fetch(query)
    

    async def _fetch(self, query: sa.sql.Select):
        objects = [obj for obj, in (await self._execute(query)).unique()]
        logger.debug(f"Fetched {len(objects)} items.")
        return objects

    async def _execute(
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
