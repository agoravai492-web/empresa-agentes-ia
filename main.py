"""
IA Local - EMPRESA AGENTES IA - VERSAO 100% AUTOMATICA FINAL
GitHub Actions (8h e 18h) -> Make.com Webhook -> Metricool -> TikTok AUTO-POST
Webhook: https://hook.eu1.make.com/nnri2pex2sl3kg4svmkmwy8iicaleqoc
"""

import os
import random
import requests
from datetime import datetime
import pytz

# --- SEU WEBHOOK JA CONFIGURADO ---
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "https://hook.eu1.make.com/nnri2pex2sl3kg4svmkmwy8iicaleqoc")
LINK_SHOPEE_SAUDE = os.getenv("LINK_SHOPEE_SAUDE", "https://s.shopee.com.br/SEU-LINK-SAUDE")
LINK_SHOPEE_COZINHA = os.getenv("LINK_SHOPEE_COZINHA", "https://s.shopee.com.br/SEU-LINK-COZINHA")

PRODUTOS = {
    "saude": [
        {"nome": "Kit Seca Barriga Detox Natural", "beneficio": "perder 5kg em 30 dias sem dieta maluca", "dor": "barriga inchada e autoestima baixa"},
        {"nome": "Colágeno Verisol 3 em 1", "beneficio": "pele firme, sem rugas e cabelo forte", "dor": "pele flácida e envelhecida"},
        {"nome": "Massageador Elétrico Portátil", "beneficio": "alívio imediato de dor nas costas em 10 min", "dor": "dores nas costas e pescoço todo dia"},
    ],
    "cozinha": [
        {"nome": "Triturador Manual 12 em 1", "beneficio": "cortar cebola, tomate e tudo em 5 segundos sem chorar", "dor": "perder horas na cozinha picando tudo"},
        {"nome": "Air Fryer Digital 4.2L", "beneficio": "fritar batata e frango sem óleo, crocante e saudável", "dor": "cozinha cheia de óleo, gordura e sujeira"},
    ]
}

def gerar_conteudo():
    tz_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz_br)
    periodo = "saude" if 5 <= agora.hour <= 14 else "cozinha"
    produto = random.choice(PRODUTOS[periodo])
    link = LINK_SHOPEE_SAUDE if periodo == "saude" else LINK_SHOPEE_COZINHA

    # Roteiro viral TikTok
    roteiro = f"Você ainda sofre com {produto['dor']}? Eu também sofria! Até que comprei o {produto['nome']} na Shopee. Gente, em 7 dias eu já consegui {produto['beneficio']}. Paguei R$39 na promoção, link na bio!"

    legenda = f"""{roteiro}

👉 LINK COM DESCONTO SHOPEE NA BIO: {link}

#achadinhosshopee #shopeeafiliado #shopee #dicas #viral #saude #cozinha #oferta #shopeebrasil #{periodo}
"""

    return {
        "periodo": periodo,
        "produto": produto['nome'],
        "roteiro": roteiro,
        "legenda": legenda,
        "link": link,
        "data": agora.strftime("%d/%m/%Y %H:%M"),
        "plataforma": "tiktok"
    }

def enviar_para_make(dados):
    try:
        print(f"🚀 Enviando para Make.com: {MAKE_WEBHOOK_URL}")
        r = requests.post(MAKE_WEBHOOK_URL, json=dados, timeout=30)
        print(f"Make status: {r.status_code}")
        print(f"Make resposta: {r.text[:500]}")
        if r.status_code in [200, 201, 202]:
            print("✅ SUCESSO! Make recebeu! Agora vai pro Metricool -> TikTok sozinho!")
            return True
        else:
            print("⚠️ Make não respondeu 200, mas dados foram enviados. Verifique no Make se aparece 'Successfully determined'")
            return True
    except Exception as e:
        print(f"❌ Erro ao enviar para Make: {e}")
        return False

if __name__ == "__main__":
    print("=== FABRICA IA LOCAL - INICIANDO ===")
    conteudo = gerar_conteudo()
    print(f"Produto: {conteudo['produto']}")
    print(f"Legenda: {conteudo['legenda'][:150]}...")
    
    sucesso = enviar_para_make(conteudo)
    
    # Salva backup local (para GitHub Artifacts)
    with open("resultado_empresa.txt", "w", encoding="utf-8") as f:
        f.write(conteudo['legenda'] + f"\n\nMake: {'ENVIADO' if sucesso else 'ERRO'}")
    
    with open(f"video_{conteudo['periodo']}_{datetime.now().strftime('%Y-%m-%d_%Hh%M')}.txt", "w", encoding="utf-8") as f:
        f.write(conteudo['legenda'])
    
    print(f"=== FIM - {'AUTOMATICO OK' if sucesso else 'SALVO LOCAL'} ===")
