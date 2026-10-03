# ralph-lab — pipeline de vendas

Pipeline em Python (somente stdlib) que cruza `vendas.csv` com `lojas.csv` e gera,
na raiz do repo:

| Entregavel | Gerado por | Conteudo |
|---|---|---|
| `vendas_lojas.csv` | `pipeline/join.py` | inner join por `id_loja`, com `regiao` e `uf` |
| `pivot_receita.csv` | `pipeline/pivot.py` | receita por regiao x mes (2026-01 a 2026-06) |
| `index.html` | `pipeline/web.py` | grafico SVG inline + paragrafo de conclusao |

## Como rodar

```bash
python -m pipeline.run_all   # regenera os tres entregaveis (join -> pivot -> web)
python -m pytest -q          # suite de testes
```

## Decisoes sobre os dados

**Inner join.** O relatorio e por regiao, e a regiao vem de `lojas.csv`. Uma venda
sem loja cadastrada nao tem regiao, entao nao ha onde aloca-la sem inventar dado;
uma loja sem venda nao tem receita a reportar. Por isso usamos inner join por
`id_loja`. Os CSVs de origem ficam intactos — as exclusoes acontecem so na saida.

**3 vendas orfas (`id_loja=999`).** As vendas V00421, V00422 e V00423 apontam para a
loja 999, que nao existe em `lojas.csv`. Elas ficam fora do join: **R$ 8.120,00
descartados** (1.200 + 4.520 + 2.400). Resultado: 423 linhas de entrada, 420 de
saida, receita total no relatorio de R$ 931.274,06.

**Loja 108 (Batel/PR) ausente.** A loja 108 esta cadastrada em `lojas.csv` (regiao
Sul) mas nao tem nenhuma venda em `vendas.csv`, entao nao aparece no relatorio.

**Valores.** `receita_brl` e lido como `Decimal` (aceita `349.5` e `1200`) e so e
arredondado para 2 casas na escrita dos CSVs.
