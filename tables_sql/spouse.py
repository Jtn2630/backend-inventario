# ==============================================================
# ARQUIVO: tables_sql/spouse.py
# Entidade: Tabela do cônjuge / meeiro
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

# ==============================================================
# MODELO: SPOUSE
# ==============================================================
class Spouse(Base):
    __tablename__ = "spouse"

    id: Mapped[int] = mapped_column(primary_key=True)
    deceased_id: Mapped[int] = mapped_column(
        ForeignKey("deceased.id"),
        unique=True
    )
    name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
    identity_document: Mapped[str | None] = mapped_column(String(30), nullable=True)
    address: Mapped[str | None] = mapped_column(String(250), nullable=True)
    marriage_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    participation_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )