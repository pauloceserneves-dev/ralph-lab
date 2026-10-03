# PRD: Pipeline de vendas — CSV → join → pivot → gráfico

## Introdução

Temos dois CSVs sintéticos na raiz do repositório: `vendas.csv` (423 linhas, fato) e
`lojas.csv` (8 linhas, dimensão). Precisamos de um pipeline reprodutível em Python que
junte as duas tabelas, produza um pivot de receita por região × mês e publique uma página
estática com um gráfico e uma conclusão. Os dados têm duas armadilhas propositais que o
pipeline precisa tratar de forma explícita e documentada.

## Respostas às perguntas de esclarecimento

1. Tipo de join → **A. inner join por `id_loja`** (é o que o exercício cobra: 420 linhas).
2. Linguagem/dependências → **A. Python 3, só biblioteca padrão** (`csv`, `decimal`); `pytest` só para testes.
3. Gráfico → **B. SVG inline gerado pelo Python**, sem CDN, para a página abrir offline.
4. Critério de pronto → **A. `python -m pytest -q` inteiro verde, com ≥ 4 testes.**

## Objetivos

- `vendas_lojas.csv` na raiz com exatamente 420 linhas de dados e soma de `receita_brl` = 931274.06.
- `pivot_receita.csv` na raiz com cabeçalho exato `regiao,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06`, 4 linhas de dados.
- `index.html` na raiz com um gráfico `<svg>` da receita mensal por região e um `<p>` de conclusão com ≥ 300 caracteres.
- Suíte `pytest` com pelo menos 4 testes, todos passando.

## User Stories

### US-001: Join de vendas com lojas
**Descrição:** Como analista, quero o inner join de `vendas.csv` com `lojas.csv` por `id_loja` para ter cada venda com sua região.

**Critérios de aceite:**
- [ ] `pipeline/join.py` lê os dois CSVs da raiz e grava `vendas_lojas.csv` na raiz
- [ ] Inner join: as 3 vendas com `id_loja=999` ficam de fora; a loja 108 não aparece
- [ ] Coluna `receita_brl` mantém esse nome; colunas de lojas incluem ao menos `regiao` e `uf`
- [ ] 420 linhas de dados; soma de `receita_brl` = 931274.06 (± 0.50)
- [ ] O script imprime linhas de entrada, de saída e a receita descartada (8120.00)
- [ ] `tests/test_join.py` cobre linhas e receita total; pytest passa

### US-002: Pivot região × mês
**Descrição:** Como gestor, quero a receita por região e mês para comparar o desempenho.

**Critérios de aceite:**
- [ ] `pipeline/pivot.py` lê `vendas_lojas.csv` e grava `pivot_receita.csv` na raiz
- [ ] Cabeçalho exato `regiao,2026-01,2026-02,2026-03,2026-04,2026-05,2026-06`
- [ ] 4 linhas (Centro-Oeste, Nordeste, Sudeste, Sul) em ordem alfabética, 7 colunas
- [ ] Valores com ponto decimal e 2 casas, sem `R$` e sem separador de milhar; arredondar só ao escrever
- [ ] Soma de todas as células = 931274.06 (± 0.50); Sudeste soma 265077.49
- [ ] `tests/test_pivot.py` cobre cabeçalho, forma e total; pytest passa

### US-003: Página com gráfico e conclusão
**Descrição:** Como leitor do relatório, quero uma página estática com o gráfico e uma conclusão.

**Critérios de aceite:**
- [ ] `pipeline/web.py` lê `pivot_receita.csv` e grava `index.html` na raiz
- [ ] Gráfico em `<svg>` inline (linhas ou barras agrupadas), uma série por região, legenda e eixos rotulados
- [ ] Sem scripts ou CSS externos
- [ ] `<p>` de conclusão com ≥ 300 caracteres citando região líder, receita total e as exclusões do inner join
- [ ] `tests/test_web.py` confere `<svg>` e o tamanho do `<p>`; pytest passa

### US-004: Orquestração e documentação
**Descrição:** Como mantenedor, quero um comando único e um README que explique as decisões.

**Critérios de aceite:**
- [ ] `pipeline/run_all.py` roda join → pivot → web em sequência
- [ ] `README.md` documenta o tipo de join, as 3 vendas órfãs (R$ 8.120,00 descartados) e a loja 108 fora do relatório
- [ ] `python -m pytest -q` com ≥ 4 testes, todos verdes

## Requisitos funcionais

- FR-1: Ler `receita_brl` como número (`Decimal`), aceitando `349.5` e `1200`.
- FR-2: Agrupar por mês com `data[:7]` (`YYYY-MM`).
- FR-3: Não editar, apagar ou "consertar" linhas dos CSVs de origem.
- FR-4: Não inventar dados nem valores.

## Fora de escopo

- Left join, dashboards interativos, bibliotecas externas (pandas, Chart.js).

## Métricas de sucesso

- 420 linhas · R$ 931.274,06 · Sudeste R$ 265.077,49 · pytest verde.
