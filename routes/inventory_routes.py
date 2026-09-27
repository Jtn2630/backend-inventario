from flask_openapi3 import Tag
from sqlalchemy import select

from api_data.api_models import (
    AssetCreate,
    AssetUpdate,
    AssetView,
    DebtCreate,
    DebtUpdate,
    DebtView,
    DeceasedCreate,
    DeceasedIdQuery,
    DeceasedUpdate,
    DeceasedView,
    ErrorMessage,
    HeirCreate,
    HeirUpdate,
    HeirView,
    ITDEstimateRequest,
    ITDEstimateView,
    InventoryView,
    MessageResponse,
    PartitionSummary,
    RecordIdPath,
    SpouseCreate,
    SpouseUpdate,
    SpouseView,
)

from database.database import SessionLocal

from services.itd_rj import estimate_itd_2026

from services.partition import (
    calculate_equal_share,
    calculate_net_estate_value,
    calculate_total_asset_value,
    calculate_total_debt_value,
    calculate_total_deceased_value,
)

from tables_sql.asset import Asset
from tables_sql.debt import Debt
from tables_sql.deceased import Deceased
from tables_sql.heir import Heir
from tables_sql.spouse import Spouse


inventory_tag = Tag(
    name="Inventory",
    description="Cadastro e consulta dos dados do inventário"
)

tax_tag = Tag(
    name="ITD",
    description="Estimativa acadêmica de ITD/RJ"
)


def register_routes(app):

    # =========================================================
    # DECEASED - Falecido
    # =========================================================

    @app.post(
        "/deceased",
        tags=[inventory_tag],
        summary="Cadastrar falecido",
        responses={
            201: DeceasedView,
            500: ErrorMessage
        }
    )
    def create_deceased(body: DeceasedCreate):
        with SessionLocal() as session:
            deceased = Deceased(
                **body.model_dump()
            )

            session.add(deceased)
            session.commit()
            session.refresh(deceased)

            return (
                DeceasedView
                .model_validate(deceased)
                .model_dump(mode="json"),
                201
            )

    @app.put(
        "/deceased/<id>",
        tags=[inventory_tag],
        summary="Atualizar falecido",
        responses={
            200: DeceasedView,
            404: ErrorMessage
        }
    )
    def update_deceased(
        path: RecordIdPath,
        body: DeceasedUpdate
    ):
        with SessionLocal() as session:
            deceased = session.get(
                Deceased,
                path.id
            )

            if deceased is None:
                return {
                    "message": "Deceased not found."
                }, 404

            for field, value in body.model_dump().items():
                setattr(
                    deceased,
                    field,
                    value
                )

            session.commit()
            session.refresh(deceased)

            return (
                DeceasedView
                .model_validate(deceased)
                .model_dump(mode="json"),
                200
            )

    # =========================================================
    # SPOUSE - Cônjuge
    # =========================================================

    @app.post(
        "/spouse",
        tags=[inventory_tag],
        summary="Cadastrar cônjuge",
        responses={
            201: SpouseView,
            404: ErrorMessage
        }
    )
    def create_spouse(body: SpouseCreate):
        with SessionLocal() as session:
            deceased = session.get(
                Deceased,
                body.deceased_id
            )

            if deceased is None:
                return {
                    "message": "Deceased not found."
                }, 404

            spouse = Spouse(
                **body.model_dump()
            )

            session.add(spouse)
            session.commit()
            session.refresh(spouse)

            return (
                SpouseView
                .model_validate(spouse)
                .model_dump(mode="json"),
                201
            )

    @app.put(
        "/spouse/<id>",
        tags=[inventory_tag],
        summary="Atualizar cônjuge",
        responses={
            200: SpouseView,
            404: ErrorMessage
        }
    )
    def update_spouse(
        path: RecordIdPath,
        body: SpouseUpdate
    ):
        with SessionLocal() as session:
            spouse = session.get(
                Spouse,
                path.id
            )

            if spouse is None:
                return {
                    "message": "Spouse not found."
                }, 404

            for field, value in body.model_dump().items():
                setattr(
                    spouse,
                    field,
                    value
                )

            session.commit()
            session.refresh(spouse)

            return (
                SpouseView
                .model_validate(spouse)
                .model_dump(mode="json"),
                200
            )

    @app.delete(
        "/spouse/<id>",
        tags=[inventory_tag],
        summary="Excluir cônjuge",
        responses={
            200: MessageResponse,
            404: ErrorMessage
        }
    )
    def delete_spouse(path: RecordIdPath):
        with SessionLocal() as session:
            spouse = session.get(
                Spouse,
                path.id
            )

            if spouse is None:
                return {
                    "message": "Spouse not found."
                }, 404

            session.delete(spouse)
            session.commit()

            return {
                "message": "Spouse deleted."
            }, 200

    # =========================================================
    # HEIRS - Herdeiros
    # =========================================================

    @app.post(
        "/heirs",
        tags=[inventory_tag],
        summary="Cadastrar herdeiro",
        responses={
            201: HeirView,
            404: ErrorMessage
        }
    )
    def create_heir(body: HeirCreate):
        with SessionLocal() as session:
            deceased = session.get(
                Deceased,
                body.deceased_id
            )

            if deceased is None:
                return {
                    "message": "Deceased not found."
                }, 404

            heir = Heir(
                **body.model_dump()
            )

            session.add(heir)
            session.commit()
            session.refresh(heir)

            return (
                HeirView
                .model_validate(heir)
                .model_dump(mode="json"),
                201
            )

    @app.put(
        "/heirs/<id>",
        tags=[inventory_tag],
        summary="Atualizar herdeiro",
        responses={
            200: HeirView,
            404: ErrorMessage
        }
    )
    def update_heir(
        path: RecordIdPath,
        body: HeirUpdate
    ):
        with SessionLocal() as session:
            heir = session.get(
                Heir,
                path.id
            )

            if heir is None:
                return {
                    "message": "Heir not found."
                }, 404

            for field, value in body.model_dump().items():
                setattr(
                    heir,
                    field,
                    value
                )

            session.commit()
            session.refresh(heir)

            return (
                HeirView
                .model_validate(heir)
                .model_dump(mode="json"),
                200
            )

    @app.delete(
        "/heirs/<id>",
        tags=[inventory_tag],
        summary="Excluir herdeiro",
        responses={
            200: MessageResponse,
            404: ErrorMessage
        }
    )
    def delete_heir(path: RecordIdPath):
        with SessionLocal() as session:
            heir = session.get(
                Heir,
                path.id
            )

            if heir is None:
                return {
                    "message": "Heir not found."
                }, 404

            session.delete(heir)
            session.commit()

            return {
                "message": "Heir deleted."
            }, 200

    # =========================================================
    # ASSETS - Bens  
    # =========================================================

    @app.post(
        "/assets",
        tags=[inventory_tag],
        summary="Cadastrar bem",
        responses={
            201: AssetView,
            404: ErrorMessage
        }
    )
    def create_asset(body: AssetCreate):
        with SessionLocal() as session:
            deceased = session.get(
                Deceased,
                body.deceased_id
            )

            if deceased is None:
                return {
                    "message": "Deceased not found."
                }, 404

            asset = Asset(
                **body.model_dump()
            )

            session.add(asset)
            session.commit()
            session.refresh(asset)

            return (
                AssetView
                .model_validate(asset)
                .model_dump(mode="json"),
                201
            )

    @app.put(
        "/assets/<id>",
        tags=[inventory_tag],
        summary="Atualizar bem",
        responses={
            200: AssetView,
            404: ErrorMessage
        }
    )
    def update_asset(
        path: RecordIdPath,
        body: AssetUpdate
    ):
        with SessionLocal() as session:
            asset = session.get(
                Asset,
                path.id
            )

            if asset is None:
                return {
                    "message": "Asset not found."
                }, 404

            for field, value in body.model_dump().items():
                setattr(
                    asset,
                    field,
                    value
                )

            session.commit()
            session.refresh(asset)

            return (
                AssetView
                .model_validate(asset)
                .model_dump(mode="json"),
                200
            )

    @app.delete(
        "/assets/<id>",
        tags=[inventory_tag],
        summary="Excluir bem",
        responses={
            200: MessageResponse,
            404: ErrorMessage
        }
    )
    def delete_asset(path: RecordIdPath):
        with SessionLocal() as session:
            asset = session.get(
                Asset,
                path.id
            )

            if asset is None:
                return {
                    "message": "Asset not found."
                }, 404

            session.delete(asset)
            session.commit()

            return {
                "message": "Asset deleted."
            }, 200

    # =========================================================
    # DEBTS - Dívidas
    # =========================================================

    @app.post(
        "/debts",
        tags=[inventory_tag],
        summary="Cadastrar dívida",
        responses={
            201: DebtView,
            404: ErrorMessage
        }
    )
    def create_debt(body: DebtCreate):
        with SessionLocal() as session:
            deceased = session.get(
                Deceased,
                body.deceased_id
            )

            if deceased is None:
                return {
                    "message": "Deceased not found."
                }, 404

            debt = Debt(
                **body.model_dump()
            )

            session.add(debt)
            session.commit()
            session.refresh(debt)

            return (
                DebtView
                .model_validate(debt)
                .model_dump(mode="json"),
                201
            )

    @app.put(
        "/debts/<id>",
        tags=[inventory_tag],
        summary="Atualizar dívida",
        responses={
            200: DebtView,
            404: ErrorMessage
        }
    )
    def update_debt(
        path: RecordIdPath,
        body: DebtUpdate
    ):
        with SessionLocal() as session:
            debt = session.get(
                Debt,
                path.id
            )

            if debt is None:
                return {
                    "message": "Debt not found."
                }, 404

            for field, value in body.model_dump().items():
                setattr(
                    debt,
                    field,
                    value
                )

            session.commit()
            session.refresh(debt)

            return (
                DebtView
                .model_validate(debt)
                .model_dump(mode="json"),
                200
            )

    @app.delete(
        "/debts/<id>",
        tags=[inventory_tag],
        summary="Excluir dívida",
        responses={
            200: MessageResponse,
            404: ErrorMessage
        }
    )
    def delete_debt(path: RecordIdPath):
        with SessionLocal() as session:
            debt = session.get(
                Debt,
                path.id
            )

            if debt is None:
                return {
                    "message": "Debt not found."
                }, 404

            session.delete(debt)
            session.commit()

            return {
                "message": "Debt deleted."
            }, 200

    # =========================================================
    # INVENTORY - Partilha
    # =========================================================

    @app.get(
        "/inventory",
        tags=[inventory_tag],
        summary="Consultar inventário",
        responses={
            200: InventoryView,
            404: ErrorMessage
        }
    )
    def get_inventory(
        query: DeceasedIdQuery
    ):
        with SessionLocal() as session:
            deceased = session.get(
                Deceased,
                query.deceased_id
            )

            if deceased is None:
                return {
                    "message": "Deceased not found."
                }, 404

            spouse_statement = (
                select(Spouse)
                .where(
                    Spouse.deceased_id
                    == query.deceased_id
                )
            )

            spouse = session.scalar(
                spouse_statement
            )

            heirs_statement = (
                select(Heir)
                .where(
                    Heir.deceased_id
                    == query.deceased_id
                )
            )

            heirs = list(
                session
                .scalars(heirs_statement)
                .all()
            )

            assets_statement = (
                select(Asset)
                .where(
                    Asset.deceased_id
                    == query.deceased_id
                )
            )

            assets = list(
                session
                .scalars(assets_statement)
                .all()
            )

            debts_statement = (
                select(Debt)
                .where(
                    Debt.deceased_id
                    == query.deceased_id
                )
            )

            debts = list(
                session
                .scalars(debts_statement)
                .all()
            )

            total_asset_value = (
                calculate_total_asset_value(
                    assets
                )
            )

            total_deceased_value = (
                calculate_total_deceased_value(
                    assets
                )
            )

            total_debt_value = (
                calculate_total_debt_value(
                    debts
                )
            )

            net_estate_value = (
                calculate_net_estate_value(
                    total_deceased_value,
                    total_debt_value
                )
            )

            equal_share_estimate = (
                calculate_equal_share(
                    net_estate_value,
                    len(heirs)
                )
            )

            response = InventoryView(
                deceased=(
                    DeceasedView
                    .model_validate(deceased)
                ),

                spouse=(
                    SpouseView
                    .model_validate(spouse)
                    if spouse is not None
                    else None
                ),

                heirs=[
                    HeirView
                    .model_validate(heir)
                    for heir in heirs
                ],

                assets=[
                    AssetView
                    .model_validate(asset)
                    for asset in assets
                ],

                debts=[
                    DebtView
                    .model_validate(debt)
                    for debt in debts
                ],

                summary=PartitionSummary(
                    total_asset_value=(
                        total_asset_value
                    ),
                    total_deceased_value=(
                        total_deceased_value
                    ),
                    total_debt_value=(
                        total_debt_value
                    ),
                    net_estate_value=(
                        net_estate_value
                    ),
                    heirs_count=len(heirs),
                    equal_share_estimate=(
                        equal_share_estimate
                    )
                )
            )

            return response.model_dump(
                mode="json"
            )

    # =========================================================
    # ITD - Estimativa De Imposto De Transmissão Causa Mortis (RJ 2026)
    # =========================================================

    @app.post(
        "/itd-estimate",
        tags=[tax_tag],
        summary="Estimar ITD/RJ 2026",
        responses={
            200: ITDEstimateView
        }
    )
    def estimate_itd(
        body: ITDEstimateRequest
    ):
        result = estimate_itd_2026(
            body.base_value
        )

        response = ITDEstimateView(
            **result
        )

        return response.model_dump(
            mode="json"
        )