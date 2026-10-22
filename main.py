"""
IA Local - Fabrica Auto-Post Metricool + TikTok
Roda 2x por dia e POSTA SOZINHO no TikTok / Pinterest / Instagram
Via Metricool API - 100% automatico
"""

import os
import random
import requests
from datetime import datetime
import pytz

# --- SEUS SECRETS DO GITHUB ---
METRICOOL_API_KEY = os.getenv("METRICOOL_API_KEY", "")  # pega em metricool.com > Settings > API
METRICOOL_BLOG_ID = os.getenv("METRICOOL_BLOG_ID", "")  # ID do seu TikTok conectado no Metricool
LINK_SHOPEE_SAUDE = os.getenv("LINK_SHOPEE_SAUDE", "https://s.shopee.com.br/SEU-LINK-SAUDE")
LINK_SHOPEE_COZINHA = os.getenv("LINK_SHOPEE_COZINHA", "https://s.shopee.com.br/SEU-LINK-COZINHA")

PRODUTOS = {
    "saude": [
        {"nome": "Kit Seca Barriga Detox", "beneficio": "perder 5kg em 30 dias", "dor": "barriga inchada", "img": "https://cf.shopee.com.br/file/br-11134207-7r98o-lx5h5q9e0w1e1b"},
        {"nome": "Colágeno 3 em 1", "beneficio": "pele firme e sem rugas", "dor": "pele flácida", "img": "https://cf.shopee.com.br/file/br-11134207-7r98o-lx5h5q9e0w1e1b"},
        {"nome": "Massageador Elétrico", "beneficio": "alívio de dor em 10 min", "dor": "dores nas costas", "img": "https://cf.shopee.com.br/file/br-11134207-7r98o-lx5h5q9e0w1e1b"},
    ],
    "cozinha": [
        {"nome": "Triturador Manual 12 em 1", "beneficio": "cortar tudo em segundos", "dor": "perder horas picando", "img": "https://cf.shopee.com.br/file/br-11134207-7r98o-lx5h5q9e0w1e1b"},
        {"nome": "Air Fryer 4.2L Digital", "beneficio": "fritar sem óleo", "dor": "cozinha cheia de óleo", "img": "https://cf.shopee.com.br/file/br-11134207-7r98o-lx5h5q9e0w1e1b"},
    ]
}

ROTEIROS = {
    "saude": "Você sofre com {dor}? Eu sofria até descobrir {nome}. Em 7 dias já vi {beneficio}. Link na bio com desconto Shopee! #saude #shopeeafiliado",
    "cozinha": "Você ainda {dor}? Para! Com {nome} você {beneficio}. Paguei R$39 na Shopee e mudou minha vida! Link na bio! #cozinha #achadinhosshopee"
}

def get_periodo():
    tz_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz_br)
    return ("saude" if 5 <= agora.hour <= 14 else "cozinha"), agora

def postar_metricool(texto, link, imagem_url=""):
    """Tenta postar no Metricool - se não tiver chave, só salva"""
    if not METRICOOL_API_KEY or not METRICOOL_BLOG_ID:
        print("⚠️ METRICOOL_API_KEY não configurada - salvando apenas local (modo teste)")
        return False
    
    try:
        # Metricool API - endpoint de agendamento
        # Documentação: https://metricool.com/api-docs/
        url = "https://app.metricool.com/api/v2/scheduler/posts"
        headers = {
            "X-Mc-Auth": METRICOOL_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "blogId": int(METRICOOL_BLOG_ID),
            "provider": "tiktok",  # pode ser tiktok, instagram, pinterest, facebook
            "type": "post",
            "text": f"{texto}\n\n{link}",
            "media": [imagem_url] if imagem_url else [],
            "autoPublish": True,
            "date": datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
        }
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        print(f"Metricool response: {r.status_code} - {r.text[:500]}")
        return r.status_code in [200, 201]
    except Exception as e:
        print(f"Erro Metricool: {e}")
        return False

def gerar_e_postar():
    periodo, agora = get_periodo()
    produto = random.choice(PRODUTOS[periodo])
    link = LINK_SHOPEE_SAUDE if periodo == "saude" else LINK_SHOPEE_COZINHA
    
    roteiro = ROTEIROS[periodo].format(**produto)
    legenda_completa = f"{roteiro}\n\nLink com desconto: {link}\n\n#ialocal #shopeeafiliado #{periodo}"
    
    conteudo = f"""
========================================
VIDEO AUTO-POST - {periodo.upper()} - {agora.strftime('%d/%m %H:%M')}
Produto: {produto['nome']}
Link: {link}

ROTEIRO:
{roteiro}

LEGENDA COMPLETA TIKTOK:
{legenda_completa}

STATUS POSTAGEM:
"""
    
    # Tenta postar automatico
    sucesso = postar_metricool(legenda_completa, link, produto.get("img",""))
    
    if sucesso:
        conteudo += "✅ POSTADO AUTOMATICAMENTE NO TIKTOK VIA METRICOOL!\n"
        print("✅ POSTADO NO TIKTOK AUTOMATICAMENTE!")
    else:
        conteudo += "⚠️ MODO TESTE - Salvo local. Configure METRICOOL_API_KEY no GitHub Secrets para auto-post.\n"
        print("Modo teste - arquivo salvo")
    
    conteudo += "========================================\n"
    
    # Salva arquivos
    with open(f"video_{periodo}_{agora.strftime('%Y-%m-%d_%Hh%M')}.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    with open("resultado_empresa.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print(conteudo)

if __name__ == "__main__":
    gerar_e_postar()
