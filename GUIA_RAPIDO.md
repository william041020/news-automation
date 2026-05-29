# 🚀 Guia Rápido — News Automation v2.0

## Instalação Inicial

```powershell
cd C:\Users\Admin\news_automation
python -m pip install -r requirements.txt
```

---

## 📋 Configurar Automação (Task Scheduler)

### Sem Telegram (silencioso)
```powershell
# Executar como Administrador
.\setup_scheduler.ps1
```
→ Roda todo dia às 07:00, salva conteúdo localmente

### Com Telegram (envio automático)
```powershell
.\setup_scheduler.ps1 -ComTelegram
```
→ Roda às 07:00 E envia para Telegram automaticamente

### Mudar horário
```powershell
.\setup_scheduler.ps1 -HoraExecucao "14:30"
```

### Remover automação
```powershell
.\setup_scheduler.ps1 -Remover
```

---

## 💻 Usar CLI Manualmente

### Gerar conteúdo
```bash
# Feeds configurados (padrão)
python main.py run --no-telegram

# Tópico customizado
python main.py run --topic "TikTok ads" --no-telegram

# Com envio para Telegram
python main.py run
```

### Gerenciar feeds
```bash
# Listar feeds
python main.py feeds list

# Adicionar feed
python main.py feeds add "https://example.com/rss" "Meu Feed"

# Desativar feed (por ID)
python main.py feeds remove 1

# Ativar feed
python main.py feeds enable 1
```

### Ver histórico
```bash
# Últimas gerações
python main.py history list

# Conteúdo completo de um artigo (por ID)
python main.py history show 1
```

### Performance
```bash
# Registrar métricas de um post
python main.py perf log
# → Wizard interativo

# Ver análise
python main.py perf stats
```

---

## 📂 Estrutura de Arquivos

| Arquivo | Função |
|---------|--------|
| `main.py` | CLI e orquestração |
| `db.py` | SQLite (feeds, articles, performance) |
| `fetcher.py` | Busca RSS |
| `generator.py` | Geração via Groq com retry |
| `formatter.py` | Markdown + Telegram |
| `notifier.py` | Envio Telegram |
| `data.db` | Banco (criado automaticamente) |
| `output/` | Arquivos .md gerados |

---

## 🎯 Workflow Típico

### 1️⃣ Primeira execução
```powershell
python main.py run --no-telegram
```
→ Cria `data.db`, busca 3 artigos, gera conteúdo

### 2️⃣ Checar resultado
```powershell
python main.py history list
python main.py history show 1
```

### 3️⃣ Registrar performance (após postar)
```powershell
python main.py perf log
# Escolha artigo → roteiro → views/saves/likes
```

### 4️⃣ Ver análise
```powershell
python main.py perf stats
```

### 5️⃣ (Opcional) Ativar automação
```powershell
.\setup_scheduler.ps1 -ComTelegram
```

---

## 📊 Output Gerado

**Arquivo**: `output/conteudo_YYYYMMDD.md`

Contém por artigo:
- Roteiro A (Inversão + tipo)
- Roteiro B (Inversão + tipo diferente)
- Carrossel (6 slides)
- **Thread** (8 posts curtos para X/LinkedIn)
- Legenda sugerida

**Banco**: `data.db`
- Feeds dinâmicos
- Histórico de gerações
- Métricas de performance

---

## 🐛 Troubleshooting

### "Python not found"
→ Instale [python.org](https://python.org) e execute como Administrador

### "GROQ_API_KEY not found"
→ Edite `.env` e adicione sua chave de [console.groq.com](https://console.groq.com)

### "UnicodeEncodeError"
→ Já corrigido! Use `python main.py` normalmente

### Scheduler não executa
→ Testar manualmente:
```powershell
Start-ScheduledTask -TaskName "NewsAutomation_TrafegoPago"
```

---

## 🔗 Links Úteis

- Groq API: https://console.groq.com
- Telegram Bot: https://t.me/BotFather
- Python Download: https://python.org

---

**Dúvidas?** Veja `IMPLEMENTACAO.md` para detalhes técnicos.
