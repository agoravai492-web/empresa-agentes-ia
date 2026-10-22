"""
IA Local - VERSAO FINAL 100% AUTOMATICA
GitHub -> Make.com Webhook -> Metricool -> TikTok (SEM CLIQUE)
"""

import os
import random
import requests
from datetime import datetime
import pytz

# --- CONFIGURAÇÃO ---
# COLOQUE SEU WEBHOOK URL AQUI OU NO GITHUB SECRETS COMO MAKE_WEBHOOK_URL
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "COLE_SEU_LINK_HOOK_EU1_AQUI")

LINK_SHOPEE_SAUDE = os.getenv("LINK_SHOPEE_SAUDE", "https://s.shopee.com.br/SEU-LINK-SAUDE")
LINK_SHOPEE_COZINHA = os.getenv("LINK_SHOPEE_COZINHA", "https://s.shopee.com.br/SEU-LINK-COZINHA")

PRODUTOS = {
    "saude": [
        {"nome": "Kit Seca Barriga Detox", "beneficio": "perder 5kg em 30 dias", "dor": "barriga inchada e cansada"},
        {"nome": "Colágeno 3 em 1 com Verisol", "beneficio": "pele firme e sem rugas", "dor": "pele flácida"},
        {"nome": "Massageador Elétrico Profissional", "beneficio": "alívio de dor em 10 min", "dor": "dores nas costas e pescoço"},
    ],
    "cozinha": [
        {"nome": "Triturador Manual 12 em 1", "beneficio": "cortar tudo em segundos", "dor": "perder horas picando comida"},
        {"nome": "Air Fryer 4.2L Digital", "beneficio": "fritar sem óleo e sem sujeira", "dor": "cozinha cheia de óleo e gordura"},
    ]
}

def gerar_conteudo():
    tz_br = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(tz_br)
    periodo = "saude" if 5 <= agora.hour <= 14 else "cozinha"
    
    produto = random.choice(PRODUTOS[periodo])
    link = LINK_SHOPEE_SAUDE if periodo == "saude" else LINK_SHOPEE_COZINHA

    roteiro = f"""POV: Você sofre com {produto['dor']}?
Eu sofria ATÉ descobrir o {produto['nome']}.
Em 7 dias já vi: {produto['beneficio']}.
E o melhor? Paguei só R$39 na Shopee na promoção!
Link na bio com DESCONTO! Corre que acaba hoje!"""

    legenda = f"""{roteiro}

👉 LINK COM DESCONTO NA BIO: {link}

#shopee #shopeeafiliado #achadinhosshopee #{periodo} #dica #viral #shopeebrasil #oferta
"""

    return {
        "periodo": periodo,
        "produto": produto['nome'],
        "roteiro": roteiro,
        "legenda": legenda,
        "link": link,
        "data": agora.isoformat(),
        "plataforma": "tiktok"
    }

def enviar_para_make(dados):
    if "hook.eu1.make.com" not in MAKE_WEBHOOK_URL:
        print("⚠️ MAKE_WEBHOOK_URL não configurado - Cole seu link hook.eu1.make.com nos Secrets do GitHub")
        print(f"Dados que seriam enviados: {dados['legenda'][:100]}...")
        return False
    
    try:
        print(f"Enviando para Make: {MAKE_WEBHOOK_URL[:40]}...")
        r = requests.post(MAKE_WEBHOOK_URL, json=dados, timeout=30)
        print(f"Make response: {r.status_code} - {r.text[:500]}")
        if r.status_code == 200 or r.status_code == 202:
            print("✅ ENVIADO COM SUCESSO PARA O MAKE! Vai postar no TikTok sozinho!")
            return True
        return False
    except Exception as e:
        print(f"Erro ao enviar para Make: {e}")
        return False

if __name__ == "__main__":
    print("=== IA LOCAL - INICIANDO FABRICA AUTOMATICA ===")
    conteudo = gerar_conteudo()
    
    # 1. Envia para Make -> Metricool -> TikTok
    sucesso = enviar_para_make(conteudo)
    
    # 2. Salva local também (backup)
    with open("resultado_empresa.txt", "w", encoding="utf-8") as f:
        f.write(f"{conteudo['legenda']}\n\nStatus Make: {'ENVIADO' if sucesso else 'MODO TESTE'}")
    
    with open(f"video_{conteudo['periodo']}_{datetime.now().strftime('%Y-%m-%d_%Hh%M')}.txt", "w", encoding="utf-8") as f:
        f.write(conteudo['legenda'])

    print("=== FIM ===")
    print(f"Status final: {'✅ AUTOMATICO' if sucesso else '⚠️ Salvo local, configure MAKE_WEBHOOK_URL'}")
