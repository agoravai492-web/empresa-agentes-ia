import os
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("GROQ_API_KEY nao encontrada! Configure em Settings > Secrets > Actions")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=groq_key,
    temperature=0.7
)

print("=== EMPRESA DE AGENTES IA INICIADA ===")

marketing = Agent(
  role='Diretor de Marketing',
  goal='Criar nome, promessa, logo, cores e 3 anuncios (AD01, AD02, AD03)',
  backstory='Especialista em infoprodutos. Transforma publico/nicho em nome e promessa irresistivel.',
  verbose=True,
  llm=llm,
  allow_delegation=False
)

vendas = Agent(
  role='Diretor de Vendas e Recuperacao',
  goal='Criar fluxo de pagina de vendas + checkout Hotmart + recuperacao',
  backstory='Cuida da pagina de vendas e recuperacao de boleto/pix cancelado com email e WhatsApp.',
  verbose=True,
  llm=llm,
  allow_delegation=False
)

ti = Agent(
  role='TI e Automacao',
  goal='Documentar como manter a empresa rodando no GitHub Actions',
  backstory='Garante que logs e automacoes funcionem.',
  verbose=True,
  llm=llm,
  allow_delegation=False
)

task1 = Task(
  description='Para o nicho de RENDA EXTRA PARA MAES, crie NOME E PROMESSA de infoproduto, defina LOGO e CORES (hex), e crie 3 copies de anuncios AD01 AD02 AD03 para testar com R$90/dia.',
  expected_output='Nome, promessa, paleta de cores hex e 3 copies de anuncio completos.',
  agent=marketing
)

task2 = Task(
  description='Com base nos anuncios, descreva fluxo: PUBLICO/NICHO -> ANUNCIOS R$90/dia -> PAG VENDA -> CHECKOUT Hotmart. Quando APROVADO: entrega. Quando CANCELADO/BOLETO/PIX: 2 e-mails de recuperacao + 1 mensagem WhatsApp oferecendo parcelamento.',
  expected_output='Fluxo completo e textos de recuperacao prontos para usar.',
  agent=vendas
)

task3 = Task(
  description='Crie checklist simples de TI: como ver resultado, onde fica o arquivo resultado_empresa.txt, e como a automacao roda todo dia 8h.',
  expected_output='Checklist pratico de 5 passos.',
  agent=ti
)

crew = Crew(
  agents=[marketing, vendas, ti],
  tasks=[task1, task2, task3],
  process=Process.sequential,
  verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== RESULTADO FINAL ===")
    print(result)
    with open("resultado_empresa.txt", "w", encoding="utf-8") as f:
        f.write(str(result))
    print("\nArquivo resultado_empresa.txt salvo!")
