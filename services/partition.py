from decimal import Decimal

from tables_sql.asset import Asset


ZERO = Decimal("0.00")
ONE_HUNDRED = Decimal("100.00")


def calculate_asset_share(asset: Asset) -> Decimal:
    if asset.value is None:
        return ZERO

    if asset.is_condominium is False:
        percentage = ONE_HUNDRED
    elif asset.ownership_percentage is None:
        return ZERO
    else:
        percentage = asset.ownership_percentage

    return asset.value * (percentage / ONE_HUNDRED)


def calculate_total_asset_value(assets: list[Asset]) -> Decimal:
    total = ZERO

    for asset in assets:
        if asset.value is not None:
            total += asset.value

    return total


def calculate_total_deceased_value(assets: list[Asset]) -> Decimal:
    total = ZERO

    for asset in assets:
        total += calculate_asset_share(asset)

    return total


def calculate_equal_share(
    total_value: Decimal,
    heirs_count: int
) -> Decimal | None:
    if heirs_count <= 0:
        return None

    return total_value / heirs_count