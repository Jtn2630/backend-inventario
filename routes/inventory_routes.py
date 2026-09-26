from flask_openapi3 import Tag
from sqlalchemy import select

from api_data.api_models import (
    AssetCreate,
    AssetView,
    DeceasedCreate,
    DeceasedIdQuery,
    DeceasedView,
    ErrorMessage,
    HeirCreate,
    HeirView,
    ITDEstimateRequest,
    ITDEstimateView,
    InventoryView,
    PartitionSummary,
    SpouseCreate,
    SpouseView,
)
from database.database import SessionLocal
from services.itd_rj import estimate_itd_2026
from services.partition import (
    calculate_equal_share,
    calculate_total_asset_value,
    calculate_total_deceased_value,
)
from tables_sql.asset import Asset
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
            deceased = Deceased(**body.model_dump())

            session.add(deceased)
            session.commit()
            session.refresh(deceased)

            return (
                DeceasedView
                .model_validate(deceased)
                .model_dump(mode="json"),
                201
            )

    @app.post(
        "/spouse",
        tags=[inventory_tag],
        summary="Cadastrar cônjuge",
        responses={201: SpouseView, 404: ErrorMessage}
    )
    def create_spouse(body: SpouseCreate):
        with SessionLocal() as session:
            deceased = session.get(Deceased, body.deceased_id)

            if deceased is None:
                return {"message": "Deceased not found."}, 404

            spouse = Spouse(**body.model_dump())
            session.add(spouse)
            session.commit()
            session.refresh(spouse)

            return (
                SpouseView
                .model_validate(spouse)
                .model_dump(mode="json"),
                201
            )

    @app.post(
        "/heirs",
        tags=[inventory_tag],
        summary="Cadastrar herdeiro",
        responses={201: HeirView, 404: ErrorMessage}
    )
    def create_heir(body: HeirCreate):
        with SessionLocal() as session:
            deceased = session.get(Deceased, body.deceased_id)

            if deceased is None:
                return {"message": "Deceased not found."}, 404

            heir = Heir(**body.model_dump())
            session.add(heir)
            session.commit()
            session.refresh(heir)

            return (
                HeirView
                .model_validate(heir)
                .model_dump(mode="json"),
                201
            )

    @app.post(
        "/assets",
        tags=[inventory_tag],
        summary="Cadastrar bem",
        responses={201: AssetView, 404: ErrorMessage}
    )
    def create_asset(body: AssetCreate):
        with SessionLocal() as session:
            deceased = session.get(Deceased, body.deceased_id)

            if deceased is None:
                return {"message": "Deceased not found."}, 404

            asset = Asset(**body.model_dump())
            session.add(asset)
            session.commit()
            session.refresh(asset)

            return (
                AssetView
                .model_validate(asset)
                .model_dump(mode="json"),
                201
            )

    @app.get(
        "/inventory",
        tags=[inventory_tag],
        summary="Consultar inventário",
        responses={200: InventoryView, 404: ErrorMessage}
    )
    def get_inventory(query: DeceasedIdQuery):
        with SessionLocal() as session:
            deceased = session.get(Deceased, query.deceased_id)

            if deceased is None:
                return {"message": "Deceased not found."}, 404

            spouse_statement = select(Spouse).where(
                Spouse.deceased_id == query.deceased_id
            )
            spouse = session.scalar(spouse_statement)

            heirs_statement = select(Heir).where(
                Heir.deceased_id == query.deceased_id
            )
            heirs = list(session.scalars(heirs_statement).all())

            assets_statement = select(Asset).where(
                Asset.deceased_id == query.deceased_id
            )
            assets = list(session.scalars(assets_statement).all())

            total_asset_value = calculate_total_asset_value(assets)
            total_deceased_value = calculate_total_deceased_value(assets)
            equal_share_estimate = calculate_equal_share(
                total_deceased_value,
                len(heirs)
            )

            response = InventoryView(
                deceased=DeceasedView.model_validate(deceased),
                spouse=(
                    SpouseView.model_validate(spouse)
                    if spouse is not None
                    else None
                ),
                heirs=[
                    HeirView.model_validate(heir)
                    for heir in heirs
                ],
                assets=[
                    AssetView.model_validate(asset)
                    for asset in assets
                ],
                summary=PartitionSummary(
                    total_asset_value=total_asset_value,
                    total_deceased_value=total_deceased_value,
                    heirs_count=len(heirs),
                    equal_share_estimate=equal_share_estimate
                )
            )

            return response.model_dump(mode="json")

    @app.post(
        "/itd-estimate",
        tags=[tax_tag],
        summary="Estimar ITD/RJ 2026",
        responses={200: ITDEstimateView}
    )
    def estimate_itd(body: ITDEstimateRequest):
        result = estimate_itd_2026(body.base_value)
        response = ITDEstimateView(**result)

        return response.model_dump(mode="json")