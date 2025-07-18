# Agentes de Marketing com IA Generativa

Este projeto é uma aplicação web que automatiza a criação de posts de marketing com auxílio de inteligência artificial generativa (Google Gemini). Ele é composto por três serviços principais:

- **Frontend**: Interface web para o usuário.
- **Backend**: API FastAPI que coordena a aplicação.
- **Agente**: Serviço que gera textos com base em prompts, utilizando o SDK do Gemini.

A arquitetura está baseada em containers Docker, orquestrados com Kubernetes (via Helm).

---

## Como Executar (Windows e Linux)

### Pré-requisitos

- Docker e Kubernetes local instalados (ex: [Docker Desktop](https://www.docker.com/products/docker-desktop) com K8s ativado).
- O domínio `http://k8s.local` configurado no arquivo `hosts` do seu sistema:

#### No Windows

1. Edite o arquivo:
   ```
   C:\Windows\System32\drivers\etc\hosts
   ```
2. Adicione a linha:
   ```
   127.0.0.1   k8s.local
   ```

#### No Linux

Edite o arquivo `/etc/hosts` com sudo:

```bash
sudo nano /etc/hosts
```

Adicione:

```
127.0.0.1   k8s.local
```

---

### Execução

No terminal (PowerShell ou bash), execute:

```bash
cd ./script/
./build_and_load.ps1
```

Esse script irá automaticamente:

- Construir as imagens dos serviços
- Criar os manifests do Helm
- Fazer o deploy no cluster Kubernetes local

---

## Acesso

Após a execução do script, abra seu navegador e acesse:

```
http://k8s.local
```

---

## Estrutura do Projeto

```
.
├── agente_app/             # Serviço do agente com IA
├── backend/                # API FastAPI
├── frontend/               # Interface web via nginx
├── helm/                   # Chart Helm para o deploy no Kubernetes
├── docker-compose.yml      # Para ambiente local (opcional)
└── script/
    └── build_and_load.ps1  # Script de automação de build e deploy
```

---

## Autor

João Paulo Migliatti  
[github.com/Jmigliatti](https://github.com/Jmigliatti)

---