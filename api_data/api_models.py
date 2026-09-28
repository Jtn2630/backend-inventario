# ==============================================================
# ARQUIVO: api_data/api_models.py
# Schemas de validação e serialização de dados (Pydantic)
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

# ==============================================================
# PARÂMETROS DE CONSULTA E IDENTIFICADORES
# ==============================================================
class DeceasedIdQuery(BaseModel):
    deceased_id: int

class RecordIdPath(BaseModel):
    id: int

# ==============================================================
# SCHEMAS: FALECIDO (DECEASED)
# ==============================================================
class DeceasedCreate(BaseModel):
    name: str | None = None
    date_of_death: date | None = None
    cpf: str | None = None
    identity_document: str | None = None
    last_address: str | None = None
    marital_status: str | None = None
    property_regime: str | None = None
    has_will: bool | None = None

class DeceasedUpdate(BaseModel):
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

# ==============================================================
# SCHEMAS: CÔNJUGE (SPOUSE)
# ==============================================================
class SpouseCreate(BaseModel):
    deceased_id: int
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None
    marriage_date: date | None = None
    participation_percentage: Decimal | None = Field(default=None, ge=0, le=100)

class SpouseUpdate(BaseModel):
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None
    marriage_date: date | None = None
    participation_percentage: Decimal | None = Field(default=None, ge=0, le=100)

class SpouseView(SpouseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ==============================================================
# SCHEMAS: HERDEIROS (HEIRS)
# ==============================================================
class HeirCreate(BaseModel):
    deceased_id: int
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None
    kinship_degree: str | None = None

class HeirUpdate(BaseModel):
    name: str | None = None
    cpf: str | None = None
    identity_document: str | None = None
    address: str | None = None
    kinship_degree: str | None = None

class HeirView(HeirCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ==============================================================
# SCHEMAS: BENS (ASSETS)
# ==============================================================
class AssetCreate(BaseModel):
    deceased_id: int
    description: str | None = None
    value: Decimal | None = Field(default=None, ge=0)
    is_condominium: bool | None = None
    ownership_percentage: Decimal | None = Field(default=None, ge=0, le=100)
    acquisition_date: date | None = None
    is_private: bool | None = None

class AssetUpdate(BaseModel):
    description: str | None = None
    value: Decimal | None = Field(default=None, ge=0)
    is_condominium: bool | None = None
    ownership_percentage: Decimal | None = Field(default=None, ge=0, le=100)
    acquisition_date: date | None = None
    is_private: bool | None = None

class AssetView(AssetCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ==============================================================
# SCHEMAS: DÍVIDAS (DEBTS)
# ==============================================================
class DebtCreate(BaseModel):
    deceased_id: int
    description: str | None = None
    creditor: str | None = None
    value: Decimal | None = Field(default=None, ge=0)

class DebtUpdate(BaseModel):
    description: str | None = None
    creditor: str | None = None
    value: Decimal | None = Field(default=None, ge=0)

class DebtView(DebtCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ==============================================================
# SCHEMAS: PARTILHA E RESUMO
# ==============================================================
class ShareView(BaseModel):
    heir_id: int | None = None
    name: str
    quality: str
    value: Decimal

class PartitionSummary(BaseModel):
    total_asset_value: Decimal
    total_deceased_value: Decimal
    total_debt_value: Decimal
    marital_base_value: Decimal
    marital_share_value: Decimal
    estate_before_debts: Decimal
    net_estate_value: Decimal
    spouse_inheritance_value: Decimal
    spouse_total_value: Decimal
    heirs_count: int
    equal_share_estimate: Decimal | None
    shares: list[ShareView]

class InventoryView(BaseModel):
    deceased: DeceasedView
    spouse: SpouseView | None
    heirs: list[HeirView]
    assets: list[AssetView]
    debts: list[DebtView]
    summary: PartitionSummary

# ==============================================================
# SCHEMAS: ESTIMATIVA DE ITD
# ==============================================================
class ITDEstimateRequest(BaseModel):
    base_value: Decimal = Field(ge=0)

class ITDEstimateView(BaseModel):
    base_value: Decimal
    ufir_value: Decimal
    base_in_ufir: Decimal
    rate: Decimal
    estimated_tax: Decimal
    warning: str

# ==============================================================
# SCHEMAS: RESPOSTAS GENÉRICAS E ERRO
# ==============================================================
class MessageResponse(BaseModel):
    message: str

class ErrorMessage(BaseModel):
    message: str