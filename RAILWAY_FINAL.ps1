# RAILWAY FINAL SETUP
# Execute isso após Railway fazer deploy do seu código

Write-Host ""
Write-Host "=================================================="
Write-Host "NEWS AUTOMATION - RAILWAY FINAL SETUP"
Write-Host "=================================================="
Write-Host ""

Write-Host "Parabens! Seu codigo esta no GitHub!" -ForegroundColor Green
Write-Host ""
Write-Host "Agora va para Railway e execute essas 4 etapas:"
Write-Host ""

Write-Host "ETAPA 1: Conectar Railway ao GitHub" -ForegroundColor Cyan
Write-Host "  1. Abra: https://railway.app"
Write-Host "  2. Clique em 'New Project'"
Write-Host "  3. Selecione 'Deploy from GitHub Repo'"
Write-Host "  4. Procure por 'news-automation'"
Write-Host "  5. Clique em 'Deploy Now'"
Write-Host "  6. Aguarde 2-3 minutos (veja o log de deploy)"
Write-Host ""

Write-Host "ETAPA 2: Adicionar Volume (persistencia do banco)" -ForegroundColor Cyan
Write-Host "  1. Projeto Railway -> 'Storage' (lado esquerdo)"
Write-Host "  2. Clique em '+ Create Volume' ou 'Add Storage'"
Write-Host "  3. Mount Path: /data"
Write-Host "  4. Clique em 'Create'"
Write-Host ""

Write-Host "ETAPA 3: Adicionar Variaveis de Ambiente" -ForegroundColor Cyan
Write-Host "  1. Projeto Railway -> 'Variables' (lado esquerdo)"
Write-Host "  2. Para cada variavel, clique em 'Add Variable':"
Write-Host ""
Write-Host "     GROQ_API_KEY"
Write-Host "     (copie de sua .env local: GROQ_API_KEY=gsk_...)"
Write-Host ""
Write-Host "     TELEGRAM_BOT_TOKEN"
Write-Host "     (copie de sua .env local: TELEGRAM_BOT_TOKEN=8929995721:...)"
Write-Host ""
Write-Host "     TELEGRAM_CHAT_ID"
Write-Host "     (copie de sua .env local: TELEGRAM_CHAT_ID=5690186897)"
Write-Host ""
Write-Host "     DATABASE_PATH"
Write-Host "     (cole exatamente: /data/data.db)"
Write-Host ""

Write-Host "ETAPA 4: Acessar seu Dashboard" -ForegroundColor Cyan
Write-Host "  1. Projeto Railway -> 'Deployments'"
Write-Host "  2. Procure por 'Domains'"
Write-Host "  3. Clique na URL (tipo: https://news-automation-production.up.railway.app)"
Write-Host "  4. Pronto! Seu dashboard esta ONLINE!"
Write-Host ""

Write-Host "=================================================="
Write-Host "PROXIMA ETAPA: SUA URL ESTARA ATIVA 24/7!"
Write-Host "=================================================="
Write-Host ""
Write-Host "Seu dashboard agora tem:" -ForegroundColor Green
Write-Host "  - Home com cards de resumo"
Write-Host "  - Historico de artigos"
Write-Host "  - Gerenciador de feeds"
Write-Host "  - Performance analytics"
Write-Host "  - Botao 'Gerar Agora' para criar conteudo"
Write-Host "  - Banco de dados persistente!"
Write-Host ""

Write-Host "Sua automacao local continua funcionando:" -ForegroundColor Green
Write-Host "  - python main.py run (CLI)"
Write-Host "  - Task Scheduler -> Telegram (24/7)"
Write-Host ""

Write-Host "=================================================="
Write-Host "Quando terminar o setup, vem me avisar!"
Write-Host "=================================================="
Write-Host ""
