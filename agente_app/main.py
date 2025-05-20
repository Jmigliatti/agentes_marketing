from flask import Flask, request, jsonify
import os
from datetime import date
import textwrap
import warnings

# Configurações iniciais
warnings.filterwarnings("ignore")
app = Flask(__name__)

# Configura a API Key do Gemini (recomendo passar pelo docker compose)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# Imports da SDK do Gemini e ADK
from google import genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

# Função auxiliar para executar o agente e coletar resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    final_response += part.text + "\n"
    return final_response.strip()

# Funções dos 4 agentes
def agente_buscador(topico, data_hoje):
    agente = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente de pesquisa. Sua tarefa é usar a ferramenta de busca do Google para recuperar os últimos lançamentos relevantes sobre o tópico abaixo. Foque em até 5 lançamentos recentes e relevantes.
        """,
        description="Busca notícias recentes",
        tools=[google_search],
    )
    entrada = f"Tópico: {topico}\nData de hoje: {data_hoje}"
    return call_agent(agente, entrada)

def agente_planejador(topico, lancamentos):
    agente = Agent(
        name="agente_planejador",
        model="gemini-2.0-flash",
        instruction="""
        Você é um planejador de conteúdo para redes sociais. Crie um plano de post para Instagram com base nos lançamentos buscados e escolha o mais relevante.
        """,
        description="Planeja conteúdo de post",
        tools=[google_search],
    )
    entrada = f"Tópico: {topico}\nLançamentos: {lancamentos}"
    return call_agent(agente, entrada)

def agente_redator(topico, plano):
    agente = Agent(
        name="agente_redator",
        model="gemini-2.0-flash",
        instruction="""
        Você é um redator criativo. Com base no plano fornecido, escreva um post engajador para Instagram. Use linguagem simples e inclua 2 a 4 hashtags.
        """,
        description="Escreve rascunho do post"
    )
    entrada = f"Tópico: {topico}\nPlano: {plano}"
    return call_agent(agente, entrada)

def agente_revisor(topico, rascunho):
    agente = Agent(
        name="agente_revisor",
        model="gemini-2.0-flash",
        instruction="""
        Você é um revisor especializado em posts para Instagram. Revise o texto, mantendo o tom jovem e claro.
        """,
        description="Revisa o post final"
    )
    entrada = f"Tópico: {topico}\nRascunho: {rascunho}"
    return call_agent(agente, entrada)

# Rota principal da API
@app.route("/gerar-post", methods=["POST"])
def gerar_post():
    data = request.get_json()
    topico = data.get("topico", "").strip()
    if not topico:
        return jsonify({"erro": "Tópico não fornecido"}), 400

    hoje = date.today().strftime("%d/%m/%Y")
    try:
        resultado = {}

        resultado["buscador"] = agente_buscador(topico, hoje)
        resultado["planejador"] = agente_planejador(topico, resultado["buscador"])
        resultado["redator"] = agente_redator(topico, resultado["planejador"])
        resultado["revisor"] = agente_revisor(topico, resultado["redator"])

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Executa a API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
