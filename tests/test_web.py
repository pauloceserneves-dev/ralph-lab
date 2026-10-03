import re

from pipeline import join, pivot, web


def test_pagina_tem_svg_e_conclusao():
    join.main()
    pivot.main()
    web.main()
    pagina = web.SAIDA.read_text(encoding="utf-8")
    assert "<svg" in pagina and "</svg>" in pagina
    assert "<script" not in pagina and "<link" not in pagina
    for regiao in ["Centro-Oeste", "Nordeste", "Sudeste", "Sul"]:
        assert regiao in pagina
    paragrafos = re.findall(r"<p>(.*?)</p>", pagina, re.S)
    assert len(paragrafos) == 1
    conclusao = paragrafos[0]
    assert len(conclusao) >= 300
    assert "Sudeste" in conclusao
    assert "931.274,06" in conclusao
    assert "999" in conclusao and "8.120,00" in conclusao and "108" in conclusao
