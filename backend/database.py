from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from models import Base

DATABASE_URL = "postgresql://user:password@db:5432/postsdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_tabelas():
    for i in range(10):  # tenta até 10 vezes
        try:
            Base.metadata.create_all(bind=engine)
            print("Conexão com o banco bem-sucedida.")
            break
        except OperationalError as e:
            print(f"Tentativa {i+1}/10: banco ainda não está pronto, aguardando...")
            time.sleep(3)
    else:
        print("Não foi possível conectar ao banco após várias tentativas.")
        raise
