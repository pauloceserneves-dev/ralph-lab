from pipeline import run_all


def test_run_all_regenera_entregaveis():
    saidas = run_all.main()
    assert [s.name for s in saidas] == ["vendas_lojas.csv", "pivot_receita.csv", "index.html"]
    for s in saidas:
        assert s.exists() and s.stat().st_size > 0
