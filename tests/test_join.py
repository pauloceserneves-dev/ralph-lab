import csv
from decimal import Decimal

from pipeline import join


def test_join_linhas_e_receita():
    join.main()
    with open(join.SAIDA, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert len(linhas) == 420
    assert "receita_brl" in linhas[0] and "regiao" in linhas[0] and "uf" in linhas[0]
    assert all(l["id_loja"] != "999" for l in linhas)
    assert all(l["id_loja"] != "108" for l in linhas)
    total = sum(Decimal(l["receita_brl"]) for l in linhas)
    assert abs(total - Decimal("931274.06")) <= Decimal("0.50")
