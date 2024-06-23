from sqlalchemy import (
    Integer, String, Text, DateTime, Date, Float,
    ForeignKey, func
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from sqlalchemy import event, select

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now()
    )

    updated: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )
