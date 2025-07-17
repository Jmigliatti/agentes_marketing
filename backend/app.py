<<<<<<< HEAD
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
=======

from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
>>>>>>> 1980b8c (passando para kubernets)

app = Flask(__name__)
criar_tabelas()


<<<<<<< HEAD
@app.route("/gerar-post", methods=["POST"])
def gerar_post():
    topico = request.json.get("topico", "")
    res = requests.post("http://agente_app:5000/gerar-post", json={"topico": topico})
    resultado = res.json()
    salvar_post(topico, resultado['revisor'])

    return jsonify(res.json())
=======
DATABASE_URL = "postgresql://user:password@db:5432/posts_db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)

Base.metadata.create_all(bind=engine)

@app.route("/posts", methods=["GET"])
def get_posts():
    session = SessionLocal()
    posts = session.query(Post).all()
    return jsonify([{"id": p.id, "title": p.title, "content": p.content} for p in posts])
>>>>>>> 1980b8c (passando para kubernets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)