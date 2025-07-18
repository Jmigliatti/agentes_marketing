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
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "minikube tunnel"
    Write-Host "Minikube tunnel iniciado em nova janela. Deixe essa janela aberta para manter o túnel ativo."
}

# Inicia o Minikube, caso não esteja em execução
if (-not (Test-MinikubeRunning)) {
    Write-Host "Minikube não está em execução. Iniciando..."
    minikube start
    if (-not (Test-MinikubeRunning)) {
        Write-Error "Erro ao iniciar o Minikube."
        exit 1
    }
} else {
    Write-Host "Minikube já está em execução."
}

# Habilita o addon de ingress se necessário
if (-not (Test-IngressAddonEnabled)) {
    Write-Host "Habilitando o addon de ingress..."
    minikube addons enable ingress
    Start-Sleep -Seconds 15
}

# Configura o ambiente Docker local para usar o Docker interno do Minikube
minikube docker-env --shell powershell | Invoke-Expression

# Caminho base do projeto
$basePath = Resolve-Path ".."

# Build das imagens
docker build -t backend:latest (Join-Path $basePath "backend")
docker build -t frontend:latest (Join-Path $basePath "frontend")
docker build -t agente-app:latest (Join-Path $basePath "agente_app")

# Deploy com Helm
$chartPath = Join-Path $basePath "helm/agentes-marketing"
$releaseName = "agentes-marketing"

helm upgrade --install $releaseName $chartPath

# Inicia o túnel do Minikube em uma nova janela
Start-MinikubeTunnel
