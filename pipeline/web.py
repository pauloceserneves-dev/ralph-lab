"""Pagina estatica index.html com grafico SVG da receita mensal por regiao a partir de pivot_receita.csv."""
import csv
import html
from decimal import Decimal
from pathlib import Path

from pipeline import join

ROOT = Path(__file__).resolve().parent.parent
ENTRADA = ROOT / "pivot_receita.csv"
SAIDA = ROOT / "index.html"

CORES = ["#2a6fdb", "#e07a10", "#2e9e5b", "#c23b5a"]
LARGURA, ALTURA = 760, 420
MARGEM_ESQ, MARGEM_DIR, MARGEM_SUP, MARGEM_INF = 90, 170, 30, 60


def brl(valor):
    """Formata Decimal como R$ 1.234,56."""
    s = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


def ler_pivot():
    with open(ENTRADA, newline="", encoding="utf-8") as f:
        linhas = list(csv.reader(f))
    meses = linhas[0][1:]
    series = {l[0]: [Decimal(v) for v in l[1:]] for l in linhas[1:]}
    return meses, series


def exclusoes():
    """Vendas descartadas pelo inner join e lojas sem venda (le os CSVs de origem sem altera-los)."""
    vendas = join.ler_csv(join.VENDAS)
    lojas = join.ler_csv(join.LOJAS)
    _, descartadas = join.inner_join(vendas, lojas)
    ids_com_venda = {v["id_loja"].strip() for v in vendas}
    lojas_sem_venda = [l for l in lojas if l["id_loja"].strip() not in ids_com_venda]
    receita = sum((Decimal(v["receita_brl"]) for v in descartadas), Decimal("0"))
    return descartadas, receita, lojas_sem_venda


def grafico_svg(meses, series):
    area_w = LARGURA - MARGEM_ESQ - MARGEM_DIR
    area_h = ALTURA - MARGEM_SUP - MARGEM_INF
    maximo = max(v for vals in series.values() for v in vals)
    passo = Decimal("10000")
    topo = ((maximo / passo).to_integral_value(rounding="ROUND_CEILING")) * passo

    def x(i):
        return MARGEM_ESQ + area_w * i / (len(meses) - 1)

    def y(v):
        return MARGEM_SUP + area_h * (1 - float(v / topo))

    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" height="{ALTURA}" '
        f'viewBox="0 0 {LARGURA} {ALTURA}" role="img" aria-label="Receita mensal por regiao">'
    ]
    # grade e eixo Y
    marca = Decimal("0")
    while marca <= topo:
        yy = y(marca)
        partes.append(f'<line x1="{MARGEM_ESQ}" y1="{yy:.1f}" x2="{MARGEM_ESQ + area_w}" y2="{yy:.1f}" stroke="#e3e3e3"/>')
        partes.append(f'<text x="{MARGEM_ESQ - 8}" y="{yy + 4:.1f}" font-size="11" text-anchor="end">{int(marca / 1000)} mil</text>')
        marca += passo
    partes.append(f'<line x1="{MARGEM_ESQ}" y1="{MARGEM_SUP}" x2="{MARGEM_ESQ}" y2="{MARGEM_SUP + area_h}" stroke="#333"/>')
    partes.append(f'<line x1="{MARGEM_ESQ}" y1="{MARGEM_SUP + area_h}" x2="{MARGEM_ESQ + area_w}" y2="{MARGEM_SUP + area_h}" stroke="#333"/>')
    # eixo X
    for i, m in enumerate(meses):
        partes.append(f'<text x="{x(i):.1f}" y="{MARGEM_SUP + area_h + 18}" font-size="11" text-anchor="middle">{m}</text>')
    partes.append(f'<text x="{MARGEM_ESQ + area_w / 2:.1f}" y="{ALTURA - 12}" font-size="12" text-anchor="middle">Mes</text>')
    partes.append(
        f'<text x="18" y="{MARGEM_SUP + area_h / 2:.1f}" font-size="12" text-anchor="middle" '
        f'transform="rotate(-90 18 {MARGEM_SUP + area_h / 2:.1f})">Receita (R$)</text>'
    )
    # series e legenda
    for k, (regiao, vals) in enumerate(series.items()):
        cor = CORES[k % len(CORES)]
        pontos = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(vals))
        partes.append(f'<polyline points="{pontos}" fill="none" stroke="{cor}" stroke-width="2.5"/>')
        for i, v in enumerate(vals):
            partes.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.5" fill="{cor}"><title>{html.escape(regiao)} {meses[i]}: {brl(v)}</title></circle>')
        ly = MARGEM_SUP + 10 + k * 22
        lx = MARGEM_ESQ + area_w + 20
        partes.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 22}" y2="{ly}" stroke="{cor}" stroke-width="3"/>')
        partes.append(f'<text x="{lx + 30}" y="{ly + 4}" font-size="12">{html.escape(regiao)}</text>')
    partes.append("</svg>")
    return "\n".join(partes)


def conclusao(meses, series):
    totais = {r: sum(vals, Decimal("0")) for r, vals in series.items()}
    total = sum(totais.values(), Decimal("0"))
    lider = max(totais, key=totais.get)
    descartadas, receita_desc, lojas_sem_venda = exclusoes()
    ids_orfaos = sorted({v["id_loja"].strip() for v in descartadas})
    vendas_orfas = ", ".join(v["id_venda"] for v in descartadas)
    lojas_txt = ", ".join(f'{l["id_loja"]} ({l["nome_loja"]}/{l["uf"]})' for l in lojas_sem_venda)
    texto = (
        f"Entre {meses[0]} e {meses[-1]}, a receita total das vendas com loja identificada foi de {brl(total)}. "
        f"A regiao lider foi {lider}, com {brl(totais[lider])} ({totais[lider] / total * 100:.1f}% do total), "
        f"seguida por " + ", ".join(f"{r} ({brl(totais[r])})" for r in sorted(totais, key=totais.get, reverse=True)[1:]) + ". "
        f"Os numeros vem de um inner join entre vendas.csv e lojas.csv por id_loja: {len(descartadas)} vendas "
        f"({vendas_orfas}) com id_loja={', '.join(ids_orfaos)}, que nao existe no cadastro de lojas, foram excluidas, "
        f"descartando {brl(receita_desc)} de receita; "
    )
    if lojas_sem_venda:
        texto += f"e a loja {lojas_txt}, que nao tem vendas registradas, nao aparece no relatorio."
    else:
        texto += "todas as lojas cadastradas possuem vendas."
    return texto


def main():
    meses, series = ler_pivot()
    svg = grafico_svg(meses, series)
    texto = conclusao(meses, series)
    pagina = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Receita mensal por regiao</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 820px; margin: 2rem auto; color: #222; line-height: 1.5; }}
h1 {{ font-size: 1.5rem; }}
</style>
</head>
<body>
<h1>Receita mensal por regiao ({meses[0]} a {meses[-1]})</h1>
{svg}
<p>{html.escape(texto)}</p>
</body>
</html>
"""
    SAIDA.write_text(pagina, encoding="utf-8")
    return texto


if __name__ == "__main__":
    main()
