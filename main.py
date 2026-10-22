import os
from crewai import Agent, Task, Crew, Process, LLM

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    print("ERRO: GROQ_API_KEY nao encontrada")
    exit(1)

llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_key, temperature=0.7)

namer = Agent(role="Criador de Nome", goal="Criar nome de empresa impactante", backstory="Voce e especialista em naming de empresas de IA", llm=llm, verbose=True)
promesser = Agent(role="Criador de Promessa", goal="Criar promessa irresistivel", backstory="Especialista em copywriting para negocios locais", llm=llm, verbose=True)
adman = Agent(role="Criador de Anuncios", goal="Criar 3 anuncios para Instagram", backstory="Especialista em anuncios que vendem", llm=llm, verbose=True)

t1 = Task(description="Crie um nome criativo e memoravel para uma empresa de agentes de IA que vende automacao para negocios locais em Sao Carlos. Retorne so o nome e o porque.", expected_output="Nome e justificativa", agent=namer)
t2 = Task(description="Crie uma promessa irresistivel para essa empresa de IA focada em negocios locais de Sao Carlos.", expected_output="Promessa de valor clara", agent=promesser)
t3 = Task(description="Crie 3 anuncios curtos para Instagram para vender essa empresa de IA. Formato: Gancho + Corpo + CTA", expected_output="3 anuncios completos", agent=adman)

crew = Crew(agents=[namer, promesser, adman], tasks=[t1, t2, t3], process=Process.sequential, verbose=True)
result = crew.kickoff()

print("\n\n===== RESULTADO FINAL =====\n")
print(result)

with open("resultado_empresa.txt","w",encoding="utf-8") as f:
    f.write(str(result))
