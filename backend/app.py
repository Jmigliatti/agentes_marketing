from flask import Flask, request, jsonify
import requests
from database import criar_tabelas, SessionLocal
from models import Post

def salvar_post(titulo, conteudo):
    db = SessionLocal()
    novo_post = Post(titulo=titulo, conteudo=conteudo)
    db.add(novo_post)
    db.commit()
    db.close()


app = Flask(__name__)
criar_tabelas()


@app.route("/gerar-post", methods=["POST"])
def gerar_post():
    topico = request.json.get("topico", "")
    res = requests.post("http://agente_app:5000/gerar-post", json={"topico": topico})
    resultado = res.json()
    salvar_post(topico, resultado['revisor'])

    return jsonify(res.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)