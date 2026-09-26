from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class Spouse(Base):
    __tablename__ = "spouse"

    id: Mapped[int] = mapped_column(primary_key=True)
    deceased_id: Mapped[int] = mapped_column(ForeignKey("deceased.id"))
    
    name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
    identity_document: Mapped[str | None] = mapped_column(String(30), nullable=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)