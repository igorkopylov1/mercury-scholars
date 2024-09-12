import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    _repr_fields: list[str] = []
    _eq_fields: list[str] = []

    def __repr__(self) -> str:
        fields = {f"{field}={getattr(self, field)}" for field in self._repr_fields}
        return f"{self.__class__.__name__}({', '.join(fields)})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and all(
            getattr(self, field) == getattr(other, field) for field in self._eq_fields
        )


class Employees(Base):  # Test db
    __tablename__ = 'employees'
    
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    position: Mapped[str] = mapped_column(sa.String(100))
    hire_date: Mapped[sa.Date] = mapped_column(sa.Date)

    _repr_fields = ["id", "name", "position", "hire_date"]
    _eq_fields = _repr_fields


class Chat_info(Base):
    __tablename__ = 'chat_info'

    chat_id: Mapped[str] = mapped_column(sa.String(50), primary_key=True)
    first_name: Mapped[str] = mapped_column(sa.String(100))
    start_date: Mapped[sa.Date] = mapped_column(sa.Date)
    end_date: Mapped[sa.Date] = mapped_column(sa.Date)
    pay: Mapped[int] = mapped_column(sa.Integer)

    _repr_fields = ["chat_id", "first_name", "start_date", "end_date", "pay"]
    _eq_fields = _repr_fields
