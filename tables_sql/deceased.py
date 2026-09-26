from datetime import date
from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class Deceased(Base):
    __tablename__ = "deceased"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date_of_death: Mapped[date | None] = mapped_column(Date, nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
    identity_document: Mapped[str | None] = mapped_column(String(30), nullable=True)
    last_address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    marital_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    property_regime: Mapped[str | None] = mapped_column(String(100), nullable=True)
    has_will: Mapped[bool | None] = mapped_column(Boolean, nullable=True)