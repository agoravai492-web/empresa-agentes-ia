
import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
load_dotenv()

# --- DEFINIÇÃO DA EMPRESA (seus departamentos) ---
marketing = Agent(
  role='Diretor de Marketing',
  goal='Criar nome, promessa, logo, cores e 3 anuncios (AD01, AD02, AD03)',
  backstory='Você é especialista em infoprodutos. Você pega PUBLICO/NICHO e transforma em NOME E PROMESSA. Depois cria anúncios de imagem e vídeo.',
  verbose=True
)

trafego = Agent(
  role='Gestor de Tráfego',
  goal='Controlar orçamento de R$90/dia e otimizar anuncios',
  backstory='Cuida dos anúncios, sabe quando pausar um criativo ruim.'
)

vendas = Agent(
  role='Diretor de Vendas e Recuperação',
  goal='Gerenciar checkout Hotmart e recuperar CANCELADOS/BOLETO/PIX com email e WhatsApp',
  backstory='Você cuida do PÁG DE VENDA + CHECKOUT. Se APROVADO, entrega material. Se CANCELADO, envia EMAIL DE BEL e mensagem no WHATS oferecendo P.P.',
  verbose=True
)

ti = Agent(
  role='TI e Automação',
  goal='Manter a empresa no ar no GitHub',
  backstory='Garante que os logs, integrações Hotmart e WhatsApp funcionem.'
)

# --- TAREFAS (o quadro branco que você mandou) ---
task1 = Task(
  description='Para o nicho [COLE SEU NICHO AQUI - ex: "Mães que querem renda extra"], crie NOME E PROMESSA, defina LOGO e CORES, e crie 3 variações de anúncios AD01 AD02 AD03 para testar com R$90/dia. Entregue imagem + texto.',
  expected_output='Nome do produto, promessa, paleta de cores e 3 copies de anúncio.',
  agent=marketing
)

task2 = Task(
  description='Com base nos anúncios, descreva o fluxo da PÁG DE VENDA + OBRIGADO + TEC até CHECKOUT Hotmart. O que fazer quando APROVADO (RECEBE O MAT) e quando CANCELADO (BOLETO/PIX ARRASTANDO) - crie 2 e-mails de recuperação e 1 mensagem de WhatsApp oferecendo P.P.',
  expected_output='Fluxo completo e textos de recuperação.',
  agent=vendas
)

task3 = Task(
  description='Crie um checklist de TI para colocar isso no GitHub Actions rodando todo dia às 8h.',
  expected_output='Checklist simples.',
  agent=ti
)

# --- RODAR A EMPRESA ---
crew = Crew(
  agents=[marketing, vendas, ti],
  tasks=[task1, task2, task3],
  process=Process.sequential,
  verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print(result)
