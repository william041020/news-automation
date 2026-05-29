# instalar.ps1
# Script de instalacao completa da automacao
# Execute com botao direito -> "Executar com PowerShell"

Write-Host ""
Write-Host "=== Instalacao: Automacao de Noticias para Trafego Pago ==="
Write-Host ""

# ---- 1. Verifica Python ----
$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.\d+") {
            $python = $cmd
            Write-Host "[OK] Python encontrado: $ver"
            break
        }
    } catch {}
}

if (-not $python) {
    Write-Host "[!] Python 3 nao encontrado."
    Write-Host ""
    Write-Host "Opcoes para instalar Python:"
    Write-Host "  1. Site oficial (recomendado):"
    Write-Host "     Acesse: https://www.python.org/downloads/"
    Write-Host "     Baixe Python 3.11+ e marque 'Add Python to PATH' na instalacao"
    Write-Host ""
    Write-Host "  2. Via winget (terminal como Admin):"
    Write-Host "     winget install Python.Python.3.12"
    Write-Host ""
    Write-Host "Apos instalar Python, feche e reabra o PowerShell e rode este script novamente."
    Read-Host "Pressione Enter para sair"
    exit 1
}

# ---- 2. Instala dependencias ----
Write-Host ""
Write-Host "[2/4] Instalando bibliotecas Python..."
$dir = $PSScriptRoot
& $python -m pip install -r "$dir\requirements.txt" --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Falha ao instalar dependencias. Verifique sua conexao com a internet."
    Read-Host "Pressione Enter para sair"
    exit 1
}
Write-Host "[OK] Bibliotecas instaladas"

# ---- 3. Cria o .env ----
Write-Host ""
Write-Host "[3/4] Configurando variaveis de ambiente..."
$envFile = "$dir\.env"

if (Test-Path $envFile) {
    Write-Host "[OK] Arquivo .env ja existe. Nao sera sobrescrito."
} else {
    Copy-Item "$dir\.env.example" $envFile
    Write-Host "[OK] Arquivo .env criado a partir do exemplo"
    Write-Host ""
    Write-Host "IMPORTANTE: Edite o arquivo .env e preencha:"
    Write-Host "  - ANTHROPIC_API_KEY  -> https://console.anthropic.com/"
    Write-Host "  - TELEGRAM_BOT_TOKEN -> crie um bot no @BotFather no Telegram"
    Write-Host "  - TELEGRAM_CHAT_ID   -> ID do seu chat/grupo no Telegram"
    Write-Host ""
    Write-Host "Abrindo .env para edicao..."
    Start-Process notepad.exe $envFile
    Read-Host "Preencha o .env, salve, e pressione Enter para continuar"
}

# ---- 4. Agendamento ----
Write-Host ""
Write-Host "[4/4] Configurando agendamento diario (07:00)..."
try {
    & "$dir\setup_scheduler.ps1"
    Write-Host "[OK] Agendado para rodar todo dia as 07:00"
} catch {
    Write-Host "[AVISO] Nao foi possivel agendar automaticamente."
    Write-Host "  Execute manualmente como Admin: .\setup_scheduler.ps1"
}

# ---- Teste ----
Write-Host ""
Write-Host "=== Instalacao concluida! ==="
Write-Host ""
$resposta = Read-Host "Deseja rodar o script agora para testar? (s/N)"
if ($resposta -match "^[Ss]") {
    Write-Host ""
    Write-Host "Executando... (aguarde 20-30 segundos)"
    & $python "$dir\main.py"
    Write-Host ""
    Write-Host "Verifique a pasta output\ para ver o arquivo gerado."
}

Write-Host ""
Write-Host "Proximos passos:"
Write-Host "  - O script roda automaticamente todo dia as 07:00"
Write-Host "  - Arquivos salvos em: $dir\output\"
Write-Host "  - Para rodar manualmente: $python $dir\main.py"
Write-Host ""
Read-Host "Pressione Enter para sair"
