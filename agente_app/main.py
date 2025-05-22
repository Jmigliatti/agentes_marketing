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

client = genai.Client()
MODEL_ID = "gemini-2.0-flash"

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
    response = client.models.generate_content(
    model=MODEL_ID,
    contents=f"Você é um assistente de pesquisa. Sua tarefa é usar a ferramenta de busca do Google para recuperar os últimos lançamentos relevantes sobre o tópico abaixo. Foque em até 5 lançamentos recentes e relevantes.\nTópico: {topico}\nData de hoje: {data_hoje}",
    config={"tools": [{"google_search": {}}]}
)
    return response.text.strip()

def agente_planejador(topico, lancamentos):
    response = client.models.generate_content(
    model=MODEL_ID,
    contents=f"Você é um planejador de conteúdo para redes sociais. Crie um plano de post para Instagram com base nos lançamentos buscados e escolha o mais relevante. Tópico: {topico}\nLançamentos: {lancamentos}",
    config={"tools": [{"google_search": {}}]}
)
    return response.text.strip()

def agente_redator(topico, plano):
    response = client.models.generate_content(
    model=MODEL_ID,
    contents=f"Você é um redator criativo. Com base no plano fornecido, escreva um post engajador para Instagram. Use linguagem simples e inclua 2 a 4 hashtags. Tópico: {topico}\nLançamentos: {plano}",
)
    return response.text.strip()

def agente_revisor(topico, rascunho):
    response = client.models.generate_content(
    model=MODEL_ID,
    contents=f"Você é um revisor especializado em posts para Instagram. Revise o texto, mantendo o tom jovem e claro. Tópico: {topico}\nLançamentos: {rascunho}",
)
    return response.text.strip()


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
