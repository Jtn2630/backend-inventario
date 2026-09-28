# ==============================================================
# ARQUIVO: services/partition.py
# Regras de cálculo patrimonial, meação e partilha sucessória
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from decimal import Decimal

from tables_sql.asset import Asset
from tables_sql.debt import Debt
from tables_sql.heir import Heir
from tables_sql.spouse import Spouse

ZERO = Decimal("0.00")
HALF = Decimal("0.50")
ONE_HUNDRED = Decimal("100.00")

# ==============================================================
# PATRIMÔNIO E DÍVIDAS
# ==============================================================
def calculate_asset_share(asset: Asset) -> Decimal:
    """Calcula a parcela do valor do bem pertencente ao falecido."""
    if asset.value is None:
        return ZERO

    value = Decimal(asset.value)

    if asset.is_condominium is False:
        percentage = ONE_HUNDRED
    elif asset.ownership_percentage is None:
        return ZERO
    else:
        percentage = Decimal(asset.ownership_percentage)

    return (value * percentage / ONE_HUNDRED)


def calculate_total_asset_value(assets: list[Asset]) -> Decimal:
    """Soma o valor bruto de todos os bens."""
    total = ZERO
    for asset in assets:
        if asset.value is not None:
            total += Decimal(asset.value)
    return total


def calculate_total_deceased_value(assets: list[Asset]) -> Decimal:
    """Soma o valor efetivo pertencente ao falecido."""
    total = ZERO
    for asset in assets:
        total += calculate_asset_share(asset)
    return total


def calculate_total_debt_value(debts: list[Debt]) -> Decimal:
    """Soma o valor total das dívidas do espólio."""
    total = ZERO
    for debt in debts:
        if debt.value is not None:
            total += Decimal(debt.value)
    return total

# ==============================================================
# REGRAS DE MEAÇÃO DO CÔNJUGE
# ==============================================================
def asset_enters_marital_share(
    asset: Asset,
    regime: str,
    spouse: Spouse | None
) -> bool:
    """Verifica se o bem integra a meação conforme o regime."""
    if spouse is None:
        return False

    if asset.is_private is True:
        return False

    if regime == "comunhao_universal":
        return True

    if regime == "comunhao_parcial":
        if spouse.marriage_date and asset.acquisition_date:
            return asset.acquisition_date >= spouse.marriage_date
        return asset.is_private is False

    if regime == "participacao_final_aquestos":
        if spouse.marriage_date and asset.acquisition_date:
            return asset.acquisition_date >= spouse.marriage_date
        return asset.is_private is False

    if regime == "separacao_convencional":
        return False

    if regime == "separacao_obrigatoria":
        return False

    return False


def get_marital_percentage(
    regime: str,
    spouse: Spouse | None
) -> Decimal:
    """Retorna o percentual de meação aplicável."""
    if (
        regime == "participacao_final_aquestos"
        and spouse is not None
        and spouse.participation_percentage is not None
    ):
        return Decimal(spouse.participation_percentage) / ONE_HUNDRED

    return HALF


def calculate_marital_values(
    assets: list[Asset],
    regime: str,
    spouse: Spouse | None
):
    """Calcula a base de meação e o valor da meação do cônjuge."""
    marital_base = ZERO
    marital_share = ZERO
    percentage = get_marital_percentage(regime, spouse)

    for asset in assets:
        if asset_enters_marital_share(asset, regime, spouse):
            value = calculate_asset_share(asset)
            marital_base += value
            marital_share += (value * percentage)

    return (marital_base, marital_share)

# ==============================================================
# MONTE HEREDITÁRIO
# ==============================================================
def calculate_net_estate_value(
    total_deceased_value: Decimal,
    marital_share_value: Decimal,
    total_debt_value: Decimal
):
    """Calcula a herança bruta e a herança líquida após abater dívidas."""
    estate_before_debts = total_deceased_value - marital_share_value
    if estate_before_debts < ZERO:
        estate_before_debts = ZERO

    net_estate_value = estate_before_debts - total_debt_value
    if net_estate_value < ZERO:
        net_estate_value = ZERO

    return (estate_before_debts, net_estate_value)

# ==============================================================
# CLASSIFICAÇÃO DOS HERDEIROS
# ==============================================================
def classify_heir(heir: Heir):
    """Classifica o herdeiro em classe sucessória e grau."""
    degree = (heir.kinship_degree or "").strip().lower()

    if degree == "filho":
        return ("descendant", 1)
    if degree == "neto":
        return ("descendant", 2)
    if degree in ("pai", "mae"):
        return ("ascendant", 1)
    if degree == "avo":
        return ("ascendant", 2)
    if degree == "irmao":
        return ("collateral", 1)
    if degree == "sobrinho":
        return ("collateral", 2)

    return ("collateral", 3)


def select_successor_heirs(heirs: list[Heir]):
    """Seleciona a classe prioritária de herdeiros mais próximos."""
    categories = {
        "descendant": [],
        "ascendant": [],
        "collateral": []
    }

    for heir in heirs:
        category, degree = classify_heir(heir)
        categories[category].append((heir, degree))

    for category in ("descendant", "ascendant", "collateral"):
        items = categories[category]
        if not items:
            continue

        nearest_degree = min(item[1] for item in items)
        selected = [item[0] for item in items if item[1] == nearest_degree]
        return (selected, category)

    return ([], None)

# ==============================================================
# CONCORRÊNCIA DO CÔNJUGE COM DESCENDENTES
# ==============================================================
def spouse_competes_with_descendants(
    regime: str,
    assets: list[Asset]
) -> bool:
    """Determina se o cônjuge concorre com descendentes na herança."""
    if regime == "comunhao_universal":
        return False
    if regime == "separacao_obrigatoria":
        return False
    if regime == "comunhao_parcial":
        return any(asset.is_private is True for asset in assets)

    return True

# ==============================================================
# APURAÇÃO DOS QUINHÕES HEREDITÁRIOS
# ==============================================================
def calculate_inheritance_shares(
    net_estate_value: Decimal,
    heirs: list[Heir],
    spouse: Spouse | None,
    regime: str,
    assets: list[Asset]
):
    """Realiza a partilha dos quinhões entre cônjuge e herdeiros."""
    shares = []
    spouse_inheritance = ZERO
    selected_heirs, category = select_successor_heirs(heirs)

    if net_estate_value <= ZERO:
        return (spouse_inheritance, shares)

    # Concorrência com Descendentes
    if category == "descendant":
        spouse_competes = (
            spouse is not None
            and spouse_competes_with_descendants(regime, assets)
        )
        number_of_shares = len(selected_heirs)
        if spouse_competes:
            number_of_shares += 1

        if number_of_shares == 0:
            return (spouse_inheritance, shares)

        share_value = net_estate_value / Decimal(number_of_shares)

        if spouse_competes:
            spouse_inheritance = share_value
            shares.append({
                "heir_id": None,
                "name": spouse.name or "Cônjuge",
                "quality": "Cônjuge herdeiro",
                "value": spouse_inheritance
            })

        for heir in selected_heirs:
            shares.append({
                "heir_id": heir.id,
                "name": heir.name or "Herdeiro",
                "quality": heir.kinship_degree or "Descendente",
                "value": share_value
            })

        return (spouse_inheritance, shares)

    # Concorrência com Ascendentes
    if category == "ascendant":
        if spouse is None:
            share_value = net_estate_value / Decimal(len(selected_heirs))
            for heir in selected_heirs:
                shares.append({
                    "heir_id": heir.id,
                    "name": heir.name or "Herdeiro",
                    "quality": heir.kinship_degree or "Ascendente",
                    "value": share_value
                })
            return (ZERO, shares)

        first_degree = all(classify_heir(heir)[1] == 1 for heir in selected_heirs)
        if first_degree and len(selected_heirs) >= 2:
            spouse_inheritance = net_estate_value / Decimal("3")
        else:
            spouse_inheritance = net_estate_value / Decimal("2")

        remaining = net_estate_value - spouse_inheritance
        shares.append({
            "heir_id": None,
            "name": spouse.name or "Cônjuge",
            "quality": "Cônjuge herdeiro",
            "value": spouse_inheritance
        })

        share_value = remaining / Decimal(len(selected_heirs))
        for heir in selected_heirs:
            shares.append({
                "heir_id": heir.id,
                "name": heir.name or "Herdeiro",
                "quality": heir.kinship_degree or "Ascendente",
                "value": share_value
            })

        return (spouse_inheritance, shares)

    # Cônjuge herdeiro único na ausência de descendentes/ascendentes
    if spouse is not None:
        spouse_inheritance = net_estate_value
        shares.append({
            "heir_id": None,
            "name": spouse.name or "Cônjuge",
            "quality": "Cônjuge herdeiro",
            "value": spouse_inheritance
        })
        return (spouse_inheritance, shares)

    # Colaterais
    if selected_heirs:
        share_value = net_estate_value / Decimal(len(selected_heirs))
        for heir in selected_heirs:
            shares.append({
                "heir_id": heir.id,
                "name": heir.name or "Herdeiro",
                "quality": heir.kinship_degree or "Colateral",
                "value": share_value
            })

    return (ZERO, shares)

# ==============================================================
# RESUMO COMPLETO DO INVENTÁRIO
# ==============================================================
def calculate_inventory_summary(
    deceased,
    spouse,
    heirs,
    assets,
    debts
):
    """Gera todos os totais e a partilha consolidada do inventário."""
    total_asset_value = calculate_total_asset_value(assets)
    total_deceased_value = calculate_total_deceased_value(assets)
    total_debt_value = calculate_total_debt_value(debts)
    regime = deceased.property_regime or ""

    marital_base_value, marital_share_value = calculate_marital_values(assets, regime, spouse)
    estate_before_debts, net_estate_value = calculate_net_estate_value(
        total_deceased_value,
        marital_share_value,
        total_debt_value
    )

    spouse_inheritance_value, shares = calculate_inheritance_shares(
        net_estate_value,
        heirs,
        spouse,
        regime,
        assets
    )

    spouse_total_value = marital_share_value + spouse_inheritance_value
    heir_values = [item["value"] for item in shares if item["heir_id"] is not None]
    equal_share_estimate = heir_values[0] if heir_values else None

    return {
        "total_asset_value": total_asset_value,
        "total_deceased_value": total_deceased_value,
        "total_debt_value": total_debt_value,
        "marital_base_value": marital_base_value,
        "marital_share_value": marital_share_value,
        "estate_before_debts": estate_before_debts,
        "net_estate_value": net_estate_value,
        "spouse_inheritance_value": spouse_inheritance_value,
        "spouse_total_value": spouse_total_value,
        "heirs_count": len(heirs),
        "equal_share_estimate": equal_share_estimate,
        "shares": shares
    }