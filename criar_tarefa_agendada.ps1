# EXECUTE ESSE SCRIPT COMO ADMINISTRADOR
# Clique com botao direito > "Executar com PowerShell"

$batFile  = "C:\Users\Admin\news_automation\rodar_automacao.bat"
$taskName = "NewsAutomation_Telegram"

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  CRIANDO TAREFA AGENDADA - NEWS AUTOMATION" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Remove tarefa anterior se existir
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Cria componentes da tarefa
$action    = New-ScheduledTaskAction -Execute $batFile
$trigger   = New-ScheduledTaskTrigger -Daily -At "08:00AM"
$settings  = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 10) -RestartCount 2 -RestartInterval (New-TimeSpan -Minutes 5)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Gera conteudo de trafego pago diariamente e envia para o Telegram" `
    -Force

if ($?) {
    Write-Host ""
    Write-Host "TAREFA CRIADA COM SUCESSO!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Nome: $taskName" -ForegroundColor Yellow
    Write-Host "Horario: Todo dia as 08:00" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Testando agora..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $taskName
    Start-Sleep -Seconds 3
    $info = Get-ScheduledTaskInfo -TaskName $taskName
    Write-Host "Status: $($info.LastTaskResult)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verifique o log em:" -ForegroundColor Cyan
    Write-Host "  C:\Users\Admin\news_automation\logs\automacao.log" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "ERRO ao criar tarefa. Tente rodar como Administrador." -ForegroundColor Red
}

Write-Host ""
Read-Host "Pressione ENTER para fechar"
