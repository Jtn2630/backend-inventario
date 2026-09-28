# ==============================================================
# ARQUIVO: routes/inventory_routes.py
# Rotas e controladores da API do Inventário
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
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
from services.partition import calculate_inventory_summary
from tables_sql.asset import Asset
from tables_sql.debt import Debt
from tables_sql.deceased import Deceased
from tables_sql.heir import Heir
from tables_sql.spouse import Spouse

# ==============================================================
# TAGS DE DOCUMENTAÇÃO (OPENAPI / SWAGGER)
# ==============================================================
inventory_tag = Tag(
    name="Inventory",
    description="Cadastro, atualização, exclusão e consulta dos dados do inventário."
)

tax_tag = Tag(
    name="ITD",
    description="Estimativa acadêmica de ITD/RJ."
)

# ==============================================================
# REGISTRO DAS ROTAS DA API
# ==============================================================
def register_routes(app):

    # ----------------------------------------------------------
    # ROTAS DO FALECIDO
    # ----------------------------------------------------------
    @app.get(
        "/deceased",
        tags=[inventory_tag],
        summary="Listar inventários",
        description="Lista os falecidos cadastrados para permitir a seleção de inventários existentes."
    )
    def list_deceased():
        with SessionLocal() as session:
            deceased_list = list(
                session.scalars(
                    select(Deceased).order_by(Deceased.id)
                ).all()
            )
            return [
                DeceasedView.model_validate(deceased).model_dump(mode="json")
                for deceased in deceased_list
            ]

    @app.post(
        "/deceased",
        tags=[inventory_tag],
        summary="Cadastrar falecido",
        description="Cadastra os dados da pessoa autora da herança.",
        responses={201: DeceasedView, 500: ErrorMessage}
    )
    def create_deceased(body: DeceasedCreate):
        with SessionLocal() as session:
            deceased = Deceased(**body.model_dump())
            session.add(deceased)
            session.commit()
            session.refresh(deceased)
            return DeceasedView.model_validate(deceased).model_dump(mode="json"), 201

    @app.put(
        "/deceased/<int:id>",
        tags=[inventory_tag],
        summary="Atualizar falecido",
        description="Atualiza os dados de um falecido já cadastrado.",
        responses={200: DeceasedView, 404: ErrorMessage}
    )
    def update_deceased(path: RecordIdPath, body: DeceasedUpdate):
        with SessionLocal() as session:
            deceased = session.get(Deceased, path.id)
            if deceased is None:
                return {"message": "Deceased not found."}, 404

            dados = body.model_dump(exclude_unset=True)
            for campo, valor in dados.items():
                setattr(deceased, campo, valor)

            session.commit()
            session.refresh(deceased)
            return DeceasedView.model_validate(deceased).model_dump(mode="json")

    # ----------------------------------------------------------
    # ROTAS DO CÔNJUGE
    # ----------------------------------------------------------
    @app.post(
        "/spouse",
        tags=[inventory_tag],
        summary="Cadastrar cônjuge",
        description="Cadastra o cônjuge ou companheiro vinculado ao falecido.",
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
            return SpouseView.model_validate(spouse).model_dump(mode="json"), 201

    @app.put(
        "/spouse/<int:id>",
        tags=[inventory_tag],
        summary="Atualizar cônjuge",
        description="Atualiza os dados do cônjuge cadastrado.",
        responses={200: SpouseView, 404: ErrorMessage}
    )
    def update_spouse(path: RecordIdPath, body: SpouseUpdate):
        with SessionLocal() as session:
            spouse = session.get(Spouse, path.id)
            if spouse is None:
                return {"message": "Spouse not found."}, 404

            dados = body.model_dump(exclude_unset=True)
            for campo, valor in dados.items():
                setattr(spouse, campo, valor)

            session.commit()
            session.refresh(spouse)
            return SpouseView.model_validate(spouse).model_dump(mode="json")

    @app.delete(
        "/spouse/<int:id>",
        tags=[inventory_tag],
        summary="Excluir cônjuge",
        description="Exclui o cônjuge selecionado.",
        responses={200: MessageResponse, 404: ErrorMessage}
    )
    def delete_spouse(path: RecordIdPath):
        with SessionLocal() as session:
            spouse = session.get(Spouse, path.id)
            if spouse is None:
                return {"message": "Spouse not found."}, 404

            session.delete(spouse)
            session.commit()
            return {"message": "Spouse deleted."}

    # ----------------------------------------------------------
    # ROTAS DOS HERDEIROS
    # ----------------------------------------------------------
    @app.post(
        "/heirs",
        tags=[inventory_tag],
        summary="Cadastrar herdeiro",
        description="Cadastra um herdeiro vinculado ao falecido.",
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
            return HeirView.model_validate(heir).model_dump(mode="json"), 201

    @app.put(
        "/heirs/<int:id>",
        tags=[inventory_tag],
        summary="Atualizar herdeiro",
        description="Atualiza um herdeiro já cadastrado.",
        responses={200: HeirView, 404: ErrorMessage}
    )
    def update_heir(path: RecordIdPath, body: HeirUpdate):
        with SessionLocal() as session:
            heir = session.get(Heir, path.id)
            if heir is None:
                return {"message": "Heir not found."}, 404

            dados = body.model_dump(exclude_unset=True)
            for campo, valor in dados.items():
                setattr(heir, campo, valor)

            session.commit()
            session.refresh(heir)
            return HeirView.model_validate(heir).model_dump(mode="json")

    @app.delete(
        "/heirs/<int:id>",
        tags=[inventory_tag],
        summary="Excluir herdeiro",
        description="Exclui um herdeiro cadastrado.",
        responses={200: MessageResponse, 404: ErrorMessage}
    )
    def delete_heir(path: RecordIdPath):
        with SessionLocal() as session:
            heir = session.get(Heir, path.id)
            if heir is None:
                return {"message": "Heir not found."}, 404

            session.delete(heir)
            session.commit()
            return {"message": "Heir deleted."}

    # ----------------------------------------------------------
    # ROTAS DOS BENS
    # ----------------------------------------------------------
    @app.post(
        "/assets",
        tags=[inventory_tag],
        summary="Cadastrar bem",
        description="Cadastra um bem integrante do patrimônio informado.",
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
            return AssetView.model_validate(asset).model_dump(mode="json"), 201

    @app.put(
        "/assets/<int:id>",
        tags=[inventory_tag],
        summary="Atualizar bem",
        description="Atualiza um bem já cadastrado.",
        responses={200: AssetView, 404: ErrorMessage}
    )
    def update_asset(path: RecordIdPath, body: AssetUpdate):
        with SessionLocal() as session:
            asset = session.get(Asset, path.id)
            if asset is None:
                return {"message": "Asset not found."}, 404

            dados = body.model_dump(exclude_unset=True)
            for campo, valor in dados.items():
                setattr(asset, campo, valor)

            session.commit()
            session.refresh(asset)
            return AssetView.model_validate(asset).model_dump(mode="json")

    @app.delete(
        "/assets/<int:id>",
        tags=[inventory_tag],
        summary="Excluir bem",
        description="Exclui um bem do inventário.",
        responses={200: MessageResponse, 404: ErrorMessage}
    )
    def delete_asset(path: RecordIdPath):
        with SessionLocal() as session:
            asset = session.get(Asset, path.id)
            if asset is None:
                return {"message": "Asset not found."}, 404

            session.delete(asset)
            session.commit()
            return {"message": "Asset deleted."}

    # ----------------------------------------------------------
    # ROTAS DAS DÍVIDAS
    # ----------------------------------------------------------
    @app.post(
        "/debts",
        tags=[inventory_tag],
        summary="Cadastrar dívida",
        description="Cadastra uma dívida vinculada ao inventário.",
        responses={201: DebtView, 404: ErrorMessage}
    )
    def create_debt(body: DebtCreate):
        with SessionLocal() as session:
            deceased = session.get(Deceased, body.deceased_id)
            if deceased is None:
                return {"message": "Deceased not found."}, 404

            debt = Debt(**body.model_dump())
            session.add(debt)
            session.commit()
            session.refresh(debt)
            return DebtView.model_validate(debt).model_dump(mode="json"), 201

    @app.put(
        "/debts/<int:id>",
        tags=[inventory_tag],
        summary="Atualizar dívida",
        description="Atualiza uma dívida já cadastrada.",
        responses={200: DebtView, 404: ErrorMessage}
    )
    def update_debt(path: RecordIdPath, body: DebtUpdate):
        with SessionLocal() as session:
            debt = session.get(Debt, path.id)
            if debt is None:
                return {"message": "Debt not found."}, 404

            dados = body.model_dump(exclude_unset=True)
            for campo, valor in dados.items():
                setattr(debt, campo, valor)

            session.commit()
            session.refresh(debt)
            return DebtView.model_validate(debt).model_dump(mode="json")

    @app.delete(
        "/debts/<int:id>",
        tags=[inventory_tag],
        summary="Excluir dívida",
        description="Exclui uma dívida do inventário.",
        responses={200: MessageResponse, 404: ErrorMessage}
    )
    def delete_debt(path: RecordIdPath):
        with SessionLocal() as session:
            debt = session.get(Debt, path.id)
            if debt is None:
                return {"message": "Debt not found."}, 404

            session.delete(debt)
            session.commit()
            return {"message": "Debt deleted."}

    # ----------------------------------------------------------
    # CONSULTA CONSOLIDADA DO INVENTÁRIO E PARTILHA
    # ----------------------------------------------------------
    @app.get(
        "/inventory",
        tags=[inventory_tag],
        summary="Consultar inventário",
        description="Consulta o inventário completo e calcula patrimônio, meação, herança e quinhões estimados.",
        responses={200: InventoryView, 404: ErrorMessage}
    )
    def get_inventory(query: DeceasedIdQuery):
        with SessionLocal() as session:
            deceased = session.get(Deceased, query.deceased_id)
            if deceased is None:
                return {"message": "Deceased not found."}, 404

            spouse = session.scalar(
                select(Spouse).where(Spouse.deceased_id == query.deceased_id)
            )
            heirs = list(
                session.scalars(select(Heir).where(Heir.deceased_id == query.deceased_id)).all()
            )
            assets = list(
                session.scalars(select(Asset).where(Asset.deceased_id == query.deceased_id)).all()
            )
            debts = list(
                session.scalars(select(Debt).where(Debt.deceased_id == query.deceased_id)).all()
            )

            summary_data = calculate_inventory_summary(
                deceased,
                spouse,
                heirs,
                assets,
                debts
            )

            response = InventoryView(
                deceased=DeceasedView.model_validate(deceased),
                spouse=(SpouseView.model_validate(spouse) if spouse is not None else None),
                heirs=[HeirView.model_validate(heir) for heir in heirs],
                assets=[AssetView.model_validate(asset) for asset in assets],
                debts=[DebtView.model_validate(debt) for debt in debts],
                summary=PartitionSummary(**summary_data)
            )

            return response.model_dump(mode="json")

    # ----------------------------------------------------------
    # ESTIMATIVA DE ITD
    # ----------------------------------------------------------
    @app.post(
        "/itd-estimate",
        tags=[tax_tag],
        summary="Estimar ITD/RJ",
        description="Recebe uma base informada e retorna uma estimativa acadêmica do imposto.",
        responses={200: ITDEstimateView}
    )
    def estimate_itd(body: ITDEstimateRequest):
        result = estimate_itd_2026(body.base_value)
        response = ITDEstimateView(**result)
        return response.model_dump(mode="json")