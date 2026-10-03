import csv
from decimal import Decimal

from pipeline import join, pivot


def test_pivot_cabecalho_forma_e_total():
    join.main()
    pivot.main()
    with open(pivot.SAIDA, newline="", encoding="utf-8") as f:
        linhas = list(csv.reader(f))
    assert linhas[0] == ["regiao", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]
    dados = linhas[1:]
    assert len(dados) == 4
    assert all(len(l) == 7 for l in dados)
    assert [l[0] for l in dados] == ["Centro-Oeste", "Nordeste", "Sudeste", "Sul"]
    for l in dados:
        for v in l[1:]:
            assert len(v.split(".")[1]) == 2 and "," not in v
    total = sum(Decimal(v) for l in dados for v in l[1:])
    assert abs(total - Decimal("931274.06")) <= Decimal("0.50")
    sudeste = next(l for l in dados if l[0] == "Sudeste")
    assert abs(sum(Decimal(v) for v in sudeste[1:]) - Decimal("265077.49")) <= Decimal("0.50")
