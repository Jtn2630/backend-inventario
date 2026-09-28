# ==============================================================
# ARQUIVO: tables_sql/asset.py
# Entidade: Tabela de bens do espólio
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from datetime import date
from decimal import Decimal
from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

# ==============================================================
# MODELO: ASSET
# ==============================================================
class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    deceased_id: Mapped[int] = mapped_column(ForeignKey("deceased.id"))
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    is_condominium: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ownership_percentage: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    acquisition_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_private: Mapped[bool | None] = mapped_column(Boolean, nullable=True)