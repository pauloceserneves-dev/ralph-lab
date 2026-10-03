"""Inner join de vendas.csv com lojas.csv por id_loja -> vendas_lojas.csv."""
import csv
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDAS = ROOT / "vendas.csv"
LOJAS = ROOT / "lojas.csv"
SAIDA = ROOT / "vendas_lojas.csv"


def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def inner_join(vendas, lojas):
    """Retorna (linhas_juntas, linhas_descartadas)."""
    por_id = {l["id_loja"].strip(): l for l in lojas}
    juntas, descartadas = [], []
    for v in vendas:
        loja = por_id.get(v["id_loja"].strip())
        if loja is None:
            descartadas.append(v)
            continue
        juntas.append({**v, "regiao": loja["regiao"], "uf": loja["uf"]})
    return juntas, descartadas


def main():
    vendas = ler_csv(VENDAS)
    lojas = ler_csv(LOJAS)
    juntas, descartadas = inner_join(vendas, lojas)

    campos = list(vendas[0].keys()) + ["regiao", "uf"]
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(juntas)

    receita_descartada = sum((Decimal(v["receita_brl"]) for v in descartadas), Decimal("0"))
    print(f"linhas de entrada: {len(vendas)}")
    print(f"linhas de saida: {len(juntas)}")
    print(f"receita descartada: {receita_descartada:.2f}")
    return juntas, descartadas


if __name__ == "__main__":
    main()
