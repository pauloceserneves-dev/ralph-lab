"""Pivot de receita regiao x mes a partir de vendas_lojas.csv -> pivot_receita.csv."""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRADA = ROOT / "vendas_lojas.csv"
SAIDA = ROOT / "pivot_receita.csv"
MESES = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]


def pivotar(linhas):
    """Retorna {regiao: {mes: Decimal}} sem arredondar."""
    tabela = defaultdict(lambda: defaultdict(Decimal))
    for l in linhas:
        tabela[l["regiao"].strip()][l["data"].strip()[:7]] += Decimal(l["receita_brl"])
    return tabela


def main():
    with open(ENTRADA, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    tabela = pivotar(linhas)

    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["regiao"] + MESES)
        for regiao in sorted(tabela):
            w.writerow([regiao] + [f"{tabela[regiao][m]:.2f}" for m in MESES])
    return tabela


if __name__ == "__main__":
    main()
