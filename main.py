import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("ERRO: GROQ_API_KEY nao encontrada. Coloque em Settings > Secrets > Actions")
    exit(1)

client = Groq(api_key=api_key)

print("Conectando no Groq...")

prompt = """
Voce e uma agencia de marketing. Crie para uma empresa de agentes de IA que vende automacao para negocios locais em Sao Carlos, SP:

1. Um nome criativo e impactante
2. Uma promessa irresistivel (headline)
3. 3 anuncios para Instagram (Gancho + Corpo + CTA)

Seja direto e vendedor. Use portugues do Brasil.
"""

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=2000,
)

resultado = completion.choices[0].message.content

print("\n\n===== RESULTADO DA EMPRESA =====\n")
print(resultado)

with open("resultado_empresa.txt","w",encoding="utf-8") as f:
    f.write(resultado)

print("\nArquivo resultado_empresa.txt salvo com sucesso!")
