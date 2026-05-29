# Setup Railway Deploy Script
# Este script configura tudo para fazer deploy no Railway

Write-Host ""
Write-Host "=================================================="
Write-Host "SETUP RAILWAY DEPLOY - News Automation"
Write-Host "=================================================="
Write-Host ""

# Passo 1: Verificar se git está configurado
Write-Host "Passo 1: Verificando Git..." -ForegroundColor Cyan
$gitUser = git config user.name
if ($gitUser) {
    Write-Host "[OK] Git ja configurado como: $gitUser"
} else {
    Write-Host "[ERRO] Git nao esta configurado"
    Write-Host "Abra PowerShell como Admin e execute:"
    Write-Host "  git config --global user.name 'Seu Nome'"
    Write-Host "  git config --global user.email 'seu@email.com'"
    exit 1
}

# Passo 2: Pedir URL do repositório GitHub
Write-Host ""
Write-Host "Passo 2: Repositório GitHub" -ForegroundColor Cyan
Write-Host ""
Write-Host "Antes de continuar, você precisa:"
Write-Host "  1. Criar um novo repositório em: https://github.com/new"
Write-Host "  2. Nome: news-automation"
Write-Host "  3. NÃO inicialize com README"
Write-Host "  4. Copie a URL do repositório"
Write-Host ""
$githubUrl = Read-Host "Cole a URL do seu repositório GitHub"

if (-not $githubUrl.StartsWith("https://github.com")) {
    Write-Host "[ERRO] URL inválida" -ForegroundColor Red
    exit 1
}

# Passo 3: Configurar remote
Write-Host ""
Write-Host "Passo 3: Conectando ao GitHub..." -ForegroundColor Cyan
git remote remove origin 2>$null
git remote add origin $githubUrl

# Verificar
$remoteUrl = git config --get remote.origin.url
if ($remoteUrl -eq $githubUrl) {
    Write-Host "[OK] Remote configurado: $githubUrl"
} else {
    Write-Host "[ERRO] Falha ao configurar remote"
    exit 1
}

# Passo 4: Fazer push
Write-Host ""
Write-Host "Passo 4: Fazendo push para GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha no push" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:"
    Write-Host "  - Você não tem acesso ao repositório"
    Write-Host "  - Falta token de autenticação"
    Write-Host ""
    Write-Host "Solução:"
    Write-Host "  1. Abra: https://github.com/settings/tokens"
    Write-Host "  2. Gere um novo token (repo scope)"
    Write-Host "  3. Use como senha quando pedir"
    exit 1
}

Write-Host "[OK] Código enviado para GitHub!"

# Passo 5: Instruções finais
Write-Host ""
Write-Host "=================================================="
Write-Host "PROXIMO PASSO: RAILWAY DASHBOARD"
Write-Host "=================================================="
Write-Host ""
Write-Host "1. Abra: https://railway.app"
Write-Host "2. Faça login (pode usar GitHub)"
Write-Host "3. New Project → Deploy from GitHub Repo"
Write-Host "4. Selecione: news-automation"
Write-Host "5. Aguarde o deploy (2-3 minutos)"
Write-Host ""
Write-Host "DEPOIS DO DEPLOY:"
Write-Host "6. Vá para Storage → Add Volume"
Write-Host "   Mount Path: /data"
Write-Host ""
Write-Host "7. Vá para Variables → Add:"
Write-Host "   GROQ_API_KEY = gsk_xxxxx... (da sua .env)"
Write-Host "   TELEGRAM_BOT_TOKEN = 8929995721:AAHA58dx... (da sua .env)"
Write-Host "   TELEGRAM_CHAT_ID = 5690186897 (da sua .env)"
Write-Host "   DATABASE_PATH = /data/data.db"
Write-Host ""
Write-Host "8. Seu dashboard estará em uma URL tipo:"
Write-Host "   https://news-automation-production.up.railway.app"
Write-Host ""
Write-Host "=================================================="
Write-Host "SETUP CONCLUIDO!"
Write-Host "=================================================="
