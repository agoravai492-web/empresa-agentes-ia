import os
from groq import Groq

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Crie nome, promessa e 3 anuncios para empresa de agentes de IA para negocios locais em Sao Carlos"}],
    temperature=0.7,
    max_tokens=2000,
)
resultado = completion.choices[0].message.content
print(resultado)
with open("resultado_empresa.txt","w",encoding="utf-8") as f:
    f.write(resultado)
