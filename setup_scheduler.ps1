# setup_scheduler.ps1
# Configura o Windows Task Scheduler para rodar a automacao todo dia
# Execute como Administrador: clique com botao direito -> "Executar como administrador"

param(
    [string]$HoraExecucao = "07:00",  # Horario de execucao (padrao: 07:00)
    [switch]$ComTelegram = $false,     # Use -ComTelegram para enviar automaticamente para Telegram
    [switch]$Remover                   # Use -Remover para deletar a tarefa
)

$NomeTarefa = "NewsAutomation_TrafegoPago"
$DiretorioScript = $PSScriptRoot
$CaminhoScript = Join-Path $DiretorioScript "main.py"

# Descobre o Python instalado
$PythonExe = $null
$candidatos = @(
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\py.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
    "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe"
)
$pyCmd = Get-Command py -ErrorAction SilentlyContinue
if ($pyCmd) { $candidatos = @($pyCmd.Source) + $candidatos }
foreach ($c in $candidatos) {
    if ($c -and (Test-Path $c)) { $PythonExe = $c; break }
}

if (-not $PythonExe) {
    Write-Error "Python nao encontrado. Instale em python.org e tente novamente."
    exit 1
}

# --- Remover tarefa ---
if ($Remover) {
    Unregister-ScheduledTask -TaskName $NomeTarefa -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Tarefa '$NomeTarefa' removida."
    exit 0
}

# --- Criar/atualizar tarefa ---
# Monta argumento do comando run
$ComandoRun = "run"
if (-not $ComTelegram) {
    $ComandoRun += " --no-telegram"
}

$Acao = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "`"$CaminhoScript`" $ComandoRun" `
    -WorkingDirectory $DiretorioScript

$Gatilho = New-ScheduledTaskTrigger -Daily -At $HoraExecucao

$Configuracoes = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $NomeTarefa `
    -Action $Acao `
    -Trigger $Gatilho `
    -Settings $Configuracoes `
    -RunLevel Highest `
    -Force | Out-Null

$ModoTelegram = if ($ComTelegram) { "COM Telegram (enviara automaticamente)" } else { "SEM Telegram (silencioso)" }

Write-Host ""
Write-Host "Agendamento configurado com sucesso!"
Write-Host "  Tarefa    : $NomeTarefa"
Write-Host "  Script    : $CaminhoScript"
Write-Host "  Python    : $PythonExe"
Write-Host "  Horario   : todo dia as $HoraExecucao"
Write-Host "  Telegram  : $ModoTelegram"
Write-Host ""
Write-Host "Comandos uteis:"
Write-Host "  Testar agora   : Start-ScheduledTask -TaskName '$NomeTarefa'"
Write-Host "  Ver status     : Get-ScheduledTask -TaskName '$NomeTarefa'"
Write-Host "  Remover tarefa : .\setup_scheduler.ps1 -Remover"
Write-Host ""
Write-Host "Para mudar configuracoes:"
Write-Host "  Horario        : .\setup_scheduler.ps1 -HoraExecucao '08:30'"
Write-Host "  Com Telegram   : .\setup_scheduler.ps1 -ComTelegram"
Write-Host "  Sem Telegram   : .\setup_scheduler.ps1"
Write-Host ""
Write-Host "Outros comandos CLI:"
Write-Host "  Listar feeds   : python main.py feeds list"
Write-Host "  Adicionar feed : python main.py feeds add <url> <nome>"
Write-Host "  Ver historico  : python main.py history list"
Write-Host "  Performance    : python main.py perf stats"
Write-Host ""
