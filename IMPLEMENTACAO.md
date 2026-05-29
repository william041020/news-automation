# Implementação: News Automation v2.0

## Resumo das Mudanças

Sistema refatorado de um único arquivo para **arquitetura modular com CLI interativo**, integração SQLite e melhorias na geração de conteúdo.

---

## 📁 Nova Estrutura

```
news_automation/
├── main.py           # CLI com Click (entry point)
├── db.py             # Camada SQLite
├── fetcher.py        # Busca de feeds RSS
├── generator.py      # Geração via Groq com retry
├── formatter.py      # Formatação Markdown
├── notifier.py       # Envio Telegram
├── __init__.py       # Package
├── __main__.py       # Module entry point
├── requirements.txt  # Dependências (+click)
├── data.db           # Banco SQLite (criado automaticamente)
└── output/           # Arquivos .md gerados
```

---

## ✅ Recursos Implementados

### 1. **Banco de Dados SQLite** (`db.py`)
- **Tabela `feeds`**: Gerenciamento dinâmico de feeds RSS
- **Tabela `articles`**: Histórico completo de gerações com JSON do conteúdo
- **Tabela `performance`**: Rastreamento de métricas (views, saves, likes, comments)
- Seed automático com os 6 feeds iniciais

### 2. **Melhorias na Geração de Conteúdo** (`generator.py`)
- **Retry automático** (3 tentativas) com backoff exponencial para falhas JSON
- **Novo formato: Thread** (8 posts curtos para X/Twitter/LinkedIn)
- **Validação de schema**: Verifica se JSON gerado tem todas as chaves obrigatórias
- Prompt atualizado inclui instructions para o novo formato

### 3. **CLI Estruturada com Click** (`main.py`)

#### Comando: `run`
```bash
python main.py run                          # Usa feeds ativos do banco
python main.py run --topic "TikTok ads"     # Busca customizada
python main.py run --no-telegram            # Sem enviar para Telegram
```

#### Comando: `feeds`
```bash
python main.py feeds list              # Lista feeds (ativos/inativos)
python main.py feeds add <url> <nome>  # Adiciona novo feed
python main.py feeds remove <id>       # Desativa feed
python main.py feeds enable <id>       # Reativa feed
```

#### Comando: `history`
```bash
python main.py history list             # Últimas 10 gerações
python main.py history show <id>        # Exibe conteúdo completo de um artigo
```

#### Comando: `perf`
```bash
python main.py perf log                 # Wizard interativo para registrar métricas
python main.py perf stats               # Análise por tipo de roteiro, formato e tema
```

### 4. **Integração SQLite**
- Cada execução `run` salva automaticamente no banco de dados
- Histórico persistente e rastreável
- Base para análise de performance

### 5. **Novo Formato: Thread**
No output JSON agora existe:
```json
"thread": {
    "post_1": "Gancho para X/LinkedIn",
    "post_2": "Contexto do problema",
    ...
    "post_8": "CTA final"
}
```

Incluído automaticamente no Markdown gerado e preview Telegram.

---

## 🚀 Como Usar

### Instalação
```bash
cd C:\Users\Admin\news_automation
python -m pip install -r requirements.txt
```

### Primeira Execução
```bash
python main.py run --no-telegram
```

### Ver Histórico
```bash
python main.py history list
python main.py history show 1
```

### Registrar Performance
```bash
python main.py perf log        # Preenche formulário interativo
python main.py perf stats      # Vê análise
```

---

## 🔧 Atualizar Task Scheduler

O `setup_scheduler.ps1` precisa ser atualizado para chamar a CLI corretamente:

**Antes:**
```powershell
python main.py
```

**Depois:**
```powershell
python main.py run --no-telegram
```

Ou para manter full automation:
```powershell
python main.py run
```

---

## 📊 Output Gerado

**Arquivo Markdown** (ex: `conteudo_20260529.md`):
- Roteiro A + B (Inversão)
- Carrossel (6 slides)
- **Thread (novo)** — 8 posts curtos
- Legenda sugerida

**Banco de Dados** (`data.db`):
- Histórico completo
- Métricas de performance
- Gerenciamento de feeds

---

## 🎯 Próximos Passos (Opcionais)

1. **Integração Meta API** — Publicar automático no Instagram/Reels
2. **LinkedIn API** — Postar threads automaticamente
3. **Dashboard Web** — Interface visual em Flask/FastAPI
4. **Agendamento Avançado** — APScheduler para jobs em horários específicos

---

## ✨ Melhorias Técnicas

- ✅ Código modular e reutilizável
- ✅ Tratamento de Unicode (Windows console)
- ✅ Retry com exponential backoff na geração
- ✅ Relative imports + suporte para execução direta
- ✅ CLI intuitivo com Help automático
- ✅ Validação de dados antes de salvar
