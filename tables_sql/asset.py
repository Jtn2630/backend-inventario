from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base


class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    deceased_id: Mapped[int] = mapped_column(ForeignKey("deceased.id"))

    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    is_condominium: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ownership_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True
    )