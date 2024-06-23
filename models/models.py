from sqlalchemy import (
    Integer, String, Text, DateTime, Date, Float,
    ForeignKey, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from sqlalchemy import event, select

from engine import get_db
from models.Base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)  # Новое поле
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)


class Competitions(Base):
    __tablename__ = "competitions"

    competition_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=True)
    coefficient: Mapped[float] = mapped_column(Float, nullable=True)
    video_instruction: Mapped[str] = mapped_column(Text, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)


class Results(Base):
    __tablename__ = "results"

    result_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    competition_id: Mapped[int] = mapped_column(
        ForeignKey(Competitions.competition_id, ondelete="CASCADE"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"),
        nullable=False
    )

    video: Mapped[str] = mapped_column(Text, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    points: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(1), nullable=False)

    competition: Mapped["Competitions"] = relationship(
        backref="results", foreign_keys=[competition_id], cascade="all, delete"
    )

    user: Mapped["Users"] = relationship(
        backref="results", foreign_keys=[user_id], cascade="all, delete"
    )

# def calculate_points(mapper, connection, target):
#     print('da')
#     target.points = float(target.count) * 5
        


# def update_points(mapper, connection, target):
#     with Session(bind=connection) as session:
#         competition = session.query(Competitions).get(target.competition_id)
#         print(competition)
#         coefficient = competition.coefficient if competition.coefficient is not None else 1
#         target.points = float(target.count) * coefficient
#         session.flush()

# Регистрация триггера SQLAlchemy после вставки новой записи в Results

@event.listens_for(Results, 'before_update')
def update_updated_column(mapper, connection, target):
    target.points = 999999



# async_session = sessionmaker(get_db(), class_=AsyncSession)

# # Асинхронная функция для расчета points
# async def calculate_points(mapper, connection, target):
#     async with async_session() as session:
#         competition = await session.get(Competitions, target.competition_id)
#         if competition and target.count is not None:
#             coefficient = competition.coefficient if competition.coefficient is not None else 1
#             target.points = float(target.count) * coefficient
#         else:
#             target.points = None  # or target.points = 0 if you prefer 0 instead of None
#         await session.flush()

# # Асинхронная функция для обновления points
# async def update_points(mapper, connection, target):
#     async with async_session() as session:
#         competition = await session.query(Competitions).get(target.competition_id)
#         if competition and target.count is not None:
#             coefficient = competition.coefficient if competition.coefficient is not None else 1
#             target.points = float(target.count) * coefficient
#         else:
#             target.points = None  # or target.points = 0 if you prefer 0 instead of None
#         await session.flush()

# # Регистрация триггера SQLAlchemy после вставки новой записи в Results
# event.listen(Results, 'before_insert', calculate_points)

# # Регистрация триггера SQLAlchemy после обновления записи в Results
# event.listen(Results, 'after_update', update_points)


