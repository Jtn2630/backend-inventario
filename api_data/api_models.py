from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

class DeceasedIdQuery(BaseModel):
    deceased_id: int


class DeceasedCreate(BaseModel):
    name: str | None = None
    date_of_death: date | None = None
    cpf: str | None = None
    identity_document: str | None = None
    last_address: str | None = None
    marital_status: str | None = None
    property_regime: str | None = None
    has_will: bool | None = None


class DeceasedView(DeceasedCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SpouseCreate(BaseModel):
    deceased_id: int
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None

class SpouseUpdate(BaseModel):
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None


class SpouseView(SpouseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HeirCreate(BaseModel):
    deceased_id: int
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None
    kinship_degree: str | None = None

class AssetUpdate(BaseModel):
    description: str | None = None
    value: Decimal | None = Field(
        default=None,
        ge=0
    )
    is_condominium: bool | None = None
    ownership_percentage: Decimal | None = Field(
        default=None,
        ge=0,
        le=100
    )


class HeirUpdate(BaseModel):
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None
    kinship_degree: str | None = None

class HeirView(HeirCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AssetCreate(BaseModel):
    deceased_id: int
    description: str | None = None
    value: Decimal | None = Field(default=None, ge=0)
    is_condominium: bool | None = None
    ownership_percentage: Decimal | None = Field(
        default=None,
        ge=0,
        le=100
    )


class AssetView(AssetCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class DebtCreate(BaseModel):
    deceased_id: int
    description: str | None = None
    creditor: str | None = None
    value: Decimal | None = Field(
        default=None,
        ge=0
    )

class DebtUpdate(BaseModel):
    description: str | None = None
    creditor: str | None = None
    value: Decimal | None = Field(
        default=None,
        ge=0
    )


class DeceasedUpdate(BaseModel):
    name: str | None = None
    date_of_death: date | None = None
    cpf: str | None = None
    identity_document: str | None = None
    last_address: str | None = None
    marital_status: str | None = None
    property_regime: str | None = None
    has_will: bool | None = None    


class DebtView(DebtCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PartitionSummary(BaseModel):
    total_asset_value: Decimal
    total_deceased_value: Decimal
    heirs_count: int
    equal_share_estimate: Decimal | None


class InventoryView(BaseModel):
    deceased: DeceasedView
    spouse: SpouseView | None
    heirs: list[HeirView]
    assets: list[AssetView]
    summary: PartitionSummary


class ITDEstimateRequest(BaseModel):
    base_value: Decimal = Field(ge=0)


class ITDEstimateView(BaseModel):
    base_value: Decimal
    ufir_value: Decimal
    base_in_ufir: Decimal
    rate: Decimal
    estimated_tax: Decimal
    warning: str


class ErrorMessage(BaseModel):
    message: str


class RecordIdPath(BaseModel):
    id: int


class MessageResponse(BaseModel):
    message: str