"""Regenera os tres entregaveis em sequencia: join -> pivot -> web."""
from pipeline import join, pivot, web

ETAPAS = [join, pivot, web]


def main():
    for etapa in ETAPAS:
        print(f"== {etapa.__name__}")
        etapa.main()
    return [join.SAIDA, pivot.SAIDA, web.SAIDA]


if __name__ == "__main__":
    main()
