from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/gerar-post", methods=["POST"])
def gerar_post():
    topico = request.json.get("topico", "")
    res = requests.post("http://agente_app:5000/gerar-post", json={"topico": topico})
    return jsonify(res.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
