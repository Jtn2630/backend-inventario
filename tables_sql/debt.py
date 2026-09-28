# ==============================================================
# ARQUIVO: tables_sql/debt.py
# Entidade: Tabela de dívidas e encargos do espólio
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

# ==============================================================
# MODELO: DEBT
# ==============================================================
class Debt(Base):
    __tablename__ = "debt"

    id: Mapped[int] = mapped_column(primary_key=True)
    deceased_id: Mapped[int] = mapped_column(ForeignKey("deceased.id"))
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    creditor: Mapped[str | None] = mapped_column(String(100), nullable=True)
    value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)