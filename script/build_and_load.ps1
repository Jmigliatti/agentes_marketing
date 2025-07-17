# Funções de ajuda para um código mais limpo
function Test-MinikubeRunning {
    $status = minikube status --format "{{.Host}}"
    return $status -eq "Running"
}

function Test-IngressAddonEnabled {
    $addons = minikube addons list
    $ingressLine = $addons | Select-String "ingress"
    return $ingressLine -like "*enabled*"
}

function Start-MinikubeTunnel {
    # Abre o túnel em uma nova janela do PowerShell
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "minikube tunnel"
    Write-Host "Minikube tunnel iniciado em nova janela. Deixe essa janela aberta para manter o túnel ativo."
}

# --- INÍCIO DO SCRIPT ---

# 1. Verificar se o Minikube está no ar
if (-not (Test-MinikubeRunning)) {
    exit 1 # Encerra o script com um código de erro
}

# 2. Verificar se o Addon de Ingress está ativado
if (-not (Test-IngressAddonEnabled)) {
    minikube addons enable ingress
    Start-Sleep -Seconds 15 # Pausa para dar tempo ao controlador de Ingress de iniciar
}

# 3. Conectar o PowerShell ao ambiente Docker do Minikube
minikube docker-env --shell powershell | Invoke-Expression

# 4. Construir as imagens Docker
$basePath = Resolve-Path ".."
docker build -t backend:latest (Join-Path $basePath "backend")
docker build -t frontend:latest (Join-Path $basePath "frontend")
docker build -t agente-app:latest (Join-Path $basePath "agente_app")

# 5. Instalar ou Atualizar a Aplicação com Helm
$chartPath = Join-Path $basePath "helm/agentes-marketing"
$releaseName = "agentes-marketing"

helm upgrade --install $releaseName $chartPath

# 6. Iniciar o túnel Minikube
Start-MinikubeTunnel
