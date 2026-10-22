"""
IA Local - Fábrica Automática de Vídeos Afiliado
Roda 2x por dia: 8h SAÚDE / 18h COZINHA
Gera roteiros prontos pra TikTok e Pinterest
Shopee + Eduzz
"""

import os
import random
from datetime import datetime
import pytz

# --- CONFIGURAÇÃO - COLOQUE SEUS LINKS DE AFILIADO AQUI ---
# Se deixar vazio, vai usar link de exemplo
LINK_SHOPEE_SAUDE = os.getenv("LINK_SHOPEE_SAUDE", "https://s.shopee.com.br/SEU-LINK-SAUDE-AQUI")
LINK_SHOPEE_COZINHA = os.getenv("LINK_SHOPEE_COZINHA", "https://s.shopee.com.br/SEU-LINK-COZINHA-AQUI")
LINK_EDUZZ = os.getenv("LINK_EDUZZ", "https://sun.eduzz.com/SEU-LINK-EDUZZ-AQUI")

PRODUTOS = {
    "saude": [
        {"nome": "Kit Seca Barriga Detox", "beneficio": "perder 5kg em 30 dias", "dor": "barriga inchada"},
        {"nome": "Colágeno 3 em 1", "beneficio": "pele firme e sem rugas", "dor": "pele flácida"},
        {"nome": "Massageador Elétrico", "beneficio": "alívio de dor em 10 min", "dor": "dores nas costas"},
        {"nome": "Chá Detox 30 ervas", "beneficio": "desinchar e regular intestino", "dor": "inchaço"},
    ],
    "cozinha": [
        {"nome": "Triturador Manual 12 em 1", "beneficio": "cortar tudo em segundos", "dor": "perder horas picando"},
        {"nome": "Air Fryer 4.2L Digital", "beneficio": "fritar sem óleo", "dor": "cozinha cheia de óleo"},
        {"nome": "Panela Antiaderente 10pç", "beneficio": "nada gruda", "dor": "comida grudando"},
        {"nome": "Espremedor Inox", "beneficio": "suco natural em 5s", "dor": "preguiça de fazer suco"},
    ]
}

ROTEIROS_SAUDE = [
    "Você sofre com {dor}? Eu sofria até descobrir {nome}. Em 7 dias já vi {beneficio}. Link na bio com desconto Shopee!",
    "3 sinais que você precisa de {nome}: {dor}, cansaço e baixa imunidade. Testei e {beneficio}. Corre que tá em promoção!",
]

ROTEIROS_COZINHA = [
    "Você ainda {dor}? Para com isso! Com {nome} você {beneficio}. Paguei R$39 na Shopee e mudou minha vida! Link na bio!",
    "Testei 5 produtos da Shopee e SÓ ESSE valeu: {nome}. {beneficio}! Por menos de R$50. Link na bio!",
]

def get_periodo():
    tz_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz_br)
    hora = agora.hour
    # 5h às 14h = saúde, resto = cozinha
    if 5 <= hora <= 14:
        return "saude", agora
    else:
        return "cozinha", agora

def gerar_video():
    periodo, agora = get_periodo()
    produto = random.choice(PRODUTOS[periodo])
    
    if periodo == "saude":
        template = random.choice(ROTEIROS_SAUDE)
        link = LINK_SHOPEE_SAUDE
        hashtags = "#saude #shopeeafiliado #eduzz #secabarriga #dicasdesaude #bemestar"
    else:
        template = random.choice(ROTEIROS_COZINHA)
        link = LINK_SHOPEE_COZINHA
        hashtags = "#cozinha #shopeeafiliado #achadinhosshopee #donadecasa #dicasdecozinha"

    roteiro = template.format(**produto)
    
    conteudo = f"""
========================================
IA LOCAL - VIDEO AFILIADO - {periodo.upper()}
Data: {agora.strftime('%d/%m/%Y %H:%M')} Brasilia
Produto: {produto['nome']}

--- ROTEIRO TIKTOK / REELS (25s) ---
Fala: "{roteiro}"

Texto na tela:
1-5s: VOCE SOFRE COM {produto['dor'].upper()}?
6-15s: {produto['nome'].upper()}
16-25s: {produto['beneficio'].upper()}! LINK NA BIO

--- LEGENDA TIKTOK ---
{roteiro}
{hashtags}
Link: {link}

--- LEGENDA PINTEREST ---
{produto['nome']} - {produto['beneficio']}
Comprei na Shopee por preco de fabrica.
{hashtags}
Link: {link}

Link afiliado: {link}
========================================
"""
    
    nome_arquivo = f"video_{periodo}_{agora.strftime('%Y-%m-%d_%Hh%M')}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    with open("resultado_empresa.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print(f"Video gerado: {periodo} - {produto['nome']}")
    print(conteudo)

if __name__ == "__main__":
    gerar_video()
