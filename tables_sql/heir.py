# ==============================================================
# ARQUIVO: tables_sql/heir.py
# Entidade: Tabela de herdeiros
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

# ==============================================================
# MODELO: HEIR
# ==============================================================
class Heir(Base):
    __tablename__ = "heir"

    id: Mapped[int] = mapped_column(primary_key=True)
    deceased_id: Mapped[int] = mapped_column(ForeignKey("deceased.id"))
    name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
    identity_document: Mapped[str | None] = mapped_column(String(30), nullable=True)
    address: Mapped[str | None] = mapped_column(String(250), nullable=True)
    kinship_degree: Mapped[str | None] = mapped_column(String(100), nullable=True)