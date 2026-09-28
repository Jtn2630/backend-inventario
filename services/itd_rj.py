# ==============================================================
# ARQUIVO: services/itd_rj.py
# Módulo de estimativa acadêmica de ITD/RJ para 2026
# ==============================================================

# ==============================================================
# IMPORTAÇÕES NECESSÁRIAS
# ==============================================================
from decimal import Decimal

# Valor oficial da UFIR-RJ 2026
UFIR_RJ_2026 = Decimal("4.9604")

# ==============================================================
# CÁLCULOS TRIBUTÁRIOS
# ==============================================================
def get_itd_rate(base_value: Decimal) -> Decimal:
    """Calcula a alíquota de ITD com base no valor em UFIRs."""
    base_in_ufir = base_value / UFIR_RJ_2026

    if base_in_ufir <= Decimal("70000"):
        return Decimal("0.04")
    if base_in_ufir <= Decimal("100000"):
        return Decimal("0.045")
    if base_in_ufir <= Decimal("200000"):
        return Decimal("0.05")
    if base_in_ufir <= Decimal("300000"):
        return Decimal("0.06")
    if base_in_ufir <= Decimal("400000"):
        return Decimal("0.07")

    return Decimal("0.08")


def estimate_itd_2026(base_value: Decimal) -> dict:
    """Gera o resumo detalhado da estimativa do imposto."""
    rate = get_itd_rate(base_value)
    base_in_ufir = base_value / UFIR_RJ_2026
    estimated_tax = base_value * rate

    return {
        "base_value": base_value,
        "ufir_value": UFIR_RJ_2026,
        "base_in_ufir": base_in_ufir,
        "rate": rate,
        "estimated_tax": estimated_tax,
        "warning": (
            "Estimativa simplificada para fins acadêmicos. "
            "O cálculo oficial depende da legislação aplicável "
            "ao fato gerador e da apuração da SEFAZ-RJ."
        )
    }