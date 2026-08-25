"""
Gera um feed RSS 2.0 a partir da página de notícias do TRE-PE
(https://www.tre-pe.jus.br/comunicacao), sem a seção de Rádio.

Executado automaticamente pelo GitHub Actions
(.github/workflows/atualizar-feed.yml). Também pode rodar manualmente:

    pip install -r requirements.txt
    python scripts/gerar_feed_comunicacao.py

Gera/atualiza o arquivo docs/comunicacao-tre-pe.xml, publicado
automaticamente pelo GitHub Pages.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape
import os

URL_PAGINA = "https://www.tre-pe.jus.br/comunicacao"
ARQUIVO_SAIDA = os.path.join(os.path.dirname(__file__), "..", "docs", "comunicacao-tre-pe.xml")
MAX_ITENS = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}


def buscar_pagina():
    sessao = requests.Session()
    sessao.headers.update(HEADERS)
    resposta = sessao.get(URL_PAGINA, timeout=15)
    resposta.raise_for_status()
    return resposta.text


def extrair_noticias(html):
    """
    Extrai apenas os blocos de 'Notícia' da sala de imprensa,
    ignorando a seção de Rádio (que aponta para tse.jus.br).
    """
    soup = BeautifulSoup(html, "html.parser")
    noticias = []

    candidatos = soup.select("a[href*='/comunicacao/noticias/']")

    vistos = set()
    for a in candidatos:
        href = a.get("href", "")
        if href in vistos:
            continue

        titulo = a.get_text(strip=True)
        if not titulo:
            continue
        vistos.add(href)

        bloco = a.find_parent(["article", "div", "li"])
        imagem_url = None
        resumo = ""

        if bloco:
            img = bloco.find("img")
            if img and img.get("src"):
                imagem_url = img["src"]

            for p in bloco.find_all(["p", "span"]):
                texto = p.get_text(strip=True)
                if texto and texto != titulo and len(texto) > 20:
                    resumo = texto
                    break

        noticias.append({
            "titulo": titulo,
            "link": href,
            "imagem": imagem_url,
            "resumo": resumo,
        })

        if len(noticias) >= MAX_ITENS:
            break

    return noticias


def montar_rss(noticias):
    agora = format_datetime(datetime.now(timezone.utc))

    itens_xml = []
    for n in noticias:
        enclosure = ""
        if n["imagem"]:
            tipo = "image/png" if n["imagem"].lower().endswith(".png") else "image/jpeg"
            enclosure = f'<enclosure url="{escape(n["imagem"])}" type="{tipo}"/>'

        itens_xml.append(f"""
  <item>
    <title>{escape(n["titulo"])}</title>
    <link>{escape(n["link"])}</link>
    <guid isPermaLink="true">{escape(n["link"])}</guid>
    <pubDate>{agora}</pubDate>
    <description><![CDATA[{n["resumo"]}]]></description>
    {enclosure}
  </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>TRE-PE — Comunicação (Notícias)</title>
  <link>{URL_PAGINA}</link>
  <description>Feed RSS gerado automaticamente a partir das notícias publicadas na página de Comunicação do TRE-PE, sem a seção de Rádio.</description>
  <language>pt-BR</language>
  <lastBuildDate>{agora}</lastBuildDate>
  <generator>gerar_feed_comunicacao.py via GitHub Actions</generator>
{"".join(itens_xml)}
</channel>
</rss>
"""


def main():
    html = buscar_pagina()
    noticias = extrair_noticias(html)

    if not noticias:
        print("Nenhuma notícia encontrada — o layout da página pode ter mudado.")
        return

    xml = montar_rss(noticias)
    os.makedirs(os.path.dirname(ARQUIVO_SAIDA), exist_ok=True)
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"Feed gerado com {len(noticias)} notícias em {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()
