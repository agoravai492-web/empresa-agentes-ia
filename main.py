import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("ERRO: GROQ_API_KEY nao encontrada. Va em Settings > Secrets > Actions > New repository secret")
    exit(1)

client = Groq(api_key=api_key)

# Modelo novo que funciona em conta gratis em 2026
MODELO = "openai/gpt-oss-20b"

prompt = """
Voce e especialista em negocios. Crie para uma empresa de Agentes de IA que vende automacao para negocios locais em Sao Carlos, SP.

Entregue:
1. NOME da empresa - criativo, curto, memoravel
2. PROMESSA - uma frase irresistivel
3. 3 ANUNCIOS para Instagram - cada um com Gancho + Corpo + CTA

Use portugues do Brasil, direto ao ponto.
"""

print(f"Usando modelo: {MODELO}")

try:
    completion = client.chat.completions.create(
        model=MODELO,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )
    resultado = completion.choices[0].message.content
except Exception as e:
    # Fallback se o primeiro modelo falhar
    print(f"Erro com {MODELO}: {e}")
    print("Tentando modelo alternativo: llama-3.1-8b-instant")
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
        )
        resultado = completion.choices[0].message.content
    except Exception as e2:
        print(f"Segundo erro: {e2}")
        resultado = f"ERRO FINAL: {e} | {e2}"

print("\n\n===== RESULTADO =====\n")
print(resultado)

with open("resultado_empresa.txt","w",encoding="utf-8") as f:
    f.write(resultado)

print("\nArquivo resultado_empresa.txt salvo!")