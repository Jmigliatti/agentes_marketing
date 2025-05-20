from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    conteudo = Column(Text)
