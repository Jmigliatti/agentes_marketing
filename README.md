# Agentes de Marketing com IA Generativa

Este projeto é uma aplicação web containerizada que permite gerar posts de marketing com auxílio de um agente inteligente baseado em IA generativa (Google Gemini). A solução é dividida em três camadas principais: frontend, backend e agente de IA.

## 🔧 Como executar o projeto

### Pré-requisitos

- Docker
- Docker Compose

### Passos

1. Clone este repositório:
   ```bash
   git clone https://github.com/Jmigliatti/agentes_marketing.git
   cd agentes_marketing
   ```

2. Execute os containers com o Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. Acesse a aplicação em:
   - [http://localhost](http://localhost)

---

## 🧠 Ideia da aplicação

A proposta é automatizar a criação de posts para redes sociais, utilizando um agente baseado em IA generativa que responde a comandos e cria textos a partir de instruções.

O fluxo geral é:

1. O usuário acessa a interface web (frontend).
2. O frontend envia a solicitação ao backend.
3. O backend consulta o `agente_app` (que usa uma API do Google) para gerar o conteúdo.
4. O conteúdo gerado é armazenado no banco PostgreSQL (`db`).
5. O post é retornado ao usuário via frontend.

---

## 📦 Containers do Docker Compose

| Serviço      | Descrição                                                                 |
|--------------|---------------------------------------------------------------------------|
| `agente_app`  | Serviço de IA generativa com integração à API do Google (Gemini, Bard...) |
| `backend`    | API intermediária que orquestra requisições entre frontend, IA e banco    |
| `frontend`   | Interface web para os usuários gerarem seus posts                         |
| `db`         | Banco de dados PostgreSQL para persistência dos posts                     |

Todos os containers estão conectados à mesma rede Docker (`app-network`) e utilizam variáveis de ambiente para integração entre si.

---

## 🐳 Sobre o Docker Compose

O Docker Compose permite orquestrar múltiplos containers com um único comando. Neste projeto, ele:

- Cria uma rede isolada chamada `app-network`
- Define volumes persistentes para o banco PostgreSQL
- Garante a ordem de inicialização correta com `depends_on`
- Expõe as portas corretas para uso local

---
