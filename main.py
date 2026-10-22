"""
EMPRESA AGENTES IA - VERSAO ULTRA SIMPLES E RAPIDA
Funciona sozinho no GitHub - Sem Make, Sem Metricool, Sem Token
Gera 2 videos por dia - 8h saude, 18h cozinha
"""

import os
import random
from datetime import datetime
import pytz

# SEUS LINKS DA SHOPEE - TROCA AQUI
LINK_SAUDE = "https://s.shopee.com.br/SEU-LINK-SAUDE-AQUI"
LINK_COZINHA = "https://s.shopee.com.br/SEU-LINK-COZINHA-AQUI"

PRODUTOS = {
    "saude": [
        {"nome": "Kit Seca Barriga Detox", "gancho": "barriga inchada sumiu em 7 dias", "dor": "inchaço e cansaço"},
        {"nome": "Colágeno Verisol 3 em 1", "gancho": "pele esticou e ruga sumiu", "dor": "pele flácida"},
        {"nome": "Massageador Elétrico", "gancho": "dor nas costas sumiu em 10 min", "dor": "dores nas costas"},
        {"nome": "Cinta Modeladora", "gancho": "perdi 2 números em 15 dias", "dor": "gordura localizada"},
    ],
    "cozinha": [
        {"nome": "Triturador Manual 12 em 1", "gancho": "pico cebola em 5 seg sem chorar", "dor": "perder horas na cozinha"},
        {"nome": "Air Fryer 4.2L", "gancho": "frito batata sem óleo crocante", "dor": "cozinha cheia de óleo"},
        {"nome": "Jogo de Facas 6 peças", "gancho": "corta carne como manteiga", "dor": "facas cegas"},
        {"nome": "Tapete Mágico Cozinha", "gancho": "minha cozinha nunca mais sujou", "dor": "sujeira na cozinha"},
    ]
}

def gerar():
    tz = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz)
    
    # Manha = saude, Noite = cozinha
    periodo = "saude" if agora.hour < 15 else "cozinha"
    produto = random.choice(PRODUTOS[periodo])
    link = LINK_SAUDE if periodo == "saude" else LINK_COZINHA
    
    # ROTEIRO VIRAL PRONTO PRA GRAVAR
    roteiro = f"""ROTEIRO - {produto['nome']}:

[0-3s] GANCHO: "Você sofre com {produto['dor']}? Eu sofria ATÉ ontem!"

[3-10s] DOR: "Eu tentava de tudo e nada funcionava, até que..."

[10-20s] SOLUÇÃO: "Descobri o {produto['nome']} na Shopee! Olha isso: {produto['gancho']}!"

[20-25s] PROVA: "Paguei só R$39 na promoção! Tá com 50% OFF!"

[25-30s] CTA: "Link com desconto tá na bio! Corre que acaba HOJE!"
"""

    legenda = f"""Você ainda sofre com {produto['dor']}? 😱 Eu também sofria!

Até descobrir o {produto['nome']} na Shopee! 😍

👉 {produto['gancho'].upper()}!

Eu paguei só R$39, tá com 50% OFF hoje! 🔥

LINK COM DESCONTO NA BIO: {link}

#shopee #achadinhos #shopeeafiliado #viral #dica #oferta #shopeebrasil #{periodo} #promocao
"""

    return periodo, produto, roteiro, legenda, agora

if __name__ == "__main__":
    print("=== GERANDO CONTEUDO ULTRA SIMPLES ===")
    
    periodo, produto, roteiro, legenda, agora = gerar()
    
    # Cria pasta
    os.makedirs("videos_prontos", exist_ok=True)
    os.makedirs(f"videos_prontos/{agora.strftime('%Y-%m-%d')}", exist_ok=True)
    
    nome_arquivo = f"{agora.strftime('%Y-%m-%d_%Hh%M')}_{periodo}_{produto['nome'].replace(' ', '_')}"
    
    # Salva 3 arquivos prontos
    with open(f"videos_prontos/{agora.strftime('%Y-%m-%d')}/{nome_arquivo}_ROTEIRO.txt", "w", encoding="utf-8") as f:
        f.write(roteiro)
    
    with open(f"videos_prontos/{agora.strftime('%Y-%m-%d')}/{nome_arquivo}_LEGENDA.txt", "w", encoding="utf-8") as f:
        f.write(legenda)
    
    with open(f"videos_prontos/{agora.strftime('%Y-%m-%d')}/{nome_arquivo}_COMPLETO.txt", "w", encoding="utf-8") as f:
        f.write(f"{roteiro}\n\n{'='*50}\n\n{legenda}")
    
    # Salva o mais recente na raiz pra facilitar
    with open("ULTIMO_VIDEO_PRONTO.txt", "w", encoding="utf-8") as f:
        f.write(f"DATA: {agora.strftime('%d/%m/%Y %H:%M')} - {periodo.upper()}\n")
        f.write(f"PRODUTO: {produto['nome']}\n\n")
        f.write(roteiro + "\n\n" + "="*50 + "\n\n" + legenda)
    
    print(f"✅ VIDEO GERADO: {produto['nome']} - {periodo}")
    print(f"📁 Pasta: videos_prontos/{agora.strftime('%Y-%m-%d')}/")
    print("🎯 Pronto pra copiar e colar no TikTok!")
    print("=== FIM ===")
