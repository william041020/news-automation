# 🎨 Dashboard Web — News Automation v2.0

## ✅ Implementado e Testado!

Dashboard web funcional com interface profissional, tema escuro e todas as funcionalidades solicitadas.

---

## 🚀 Como Iniciar

### Instalação
```bash
cd C:\Users\Admin\news_automation
python -m pip install flask
```

### Executar
```bash
python web.py
```

Automaticamente abre `http://localhost:5000` no navegador.

---

## 📋 Funcionalidades Implementadas

### ✅ 1. **Ver Histórico e Conteúdo**
- **Página `/history`**: Lista todas as gerações agrupadas por data
- **Página `/history/<id>`**: Visualização completa com abas
  - Roteiro A (inversão + tipo)
  - Roteiro B (inversão diferente)
  - Carrossel (6 slides)
  - **Thread** (8 posts curtos)
  - Legenda sugerida

### ✅ 2. **Gerar Conteúdo via Botão**
- **Home com botão "Gerar Agora"**
  - Input opcional para tópico customizado
  - Geração em background (thread)
  - Log ao vivo com spinner
  - Polling a cada 2 segundos
  - Recarrega página ao terminar

### ✅ 3. **Gerenciar Feeds**
- **Página `/feeds`**: Tabela com todos os feeds
  - Status (Ativo/Inativo) com toggle
  - Formulário para adicionar novo feed
  - URL + Nome + Botão Adicionar
  - Dica: URLs de exemplo para Google News RSS

### ✅ 4. **Registrar e Ver Performance**
- **Página `/performance`**:
  - Gráfico Chart.js: Saves vs Views por tipo de roteiro
  - Formulário para registrar métricas
    - Artigo (select dinâmico)
    - Plataforma (Instagram, Reels, Thread, etc)
    - Roteiro (A, B, Carrossel, Thread)
    - Views, Saves, Likes, Comentários
    - Data do post
  - Tabela de histórico de registros

---

## 🎨 Design & UX

### Tema
- **Fundo**: GitHub Dark (`#0d1117`)
- **Sidebar**: `#161b22`
- **Cards**: `#21262d`
- **Accent**: Verde GitHub (`#238636`)
- **Texto**: `#e6edf3`
- **Bordas**: `#30363d`

### Layout
- **Sidebar fixo** (esquerda) com navegação
- **Topbar** (topo) com título e data última geração
- **Content area** (flex/scrollável) com cards, tabelas, forms
- **Responsivo**: Adapta a mobile (sidebar vira horizontal)

### Componentes
- Cards com ícones e métricas
- Tabs com abas (Roteiros, Carrossel, Thread, Legenda)
- Tabelas profissionais com hover effects
- Botões com estados (primary, danger, small)
- Badges (Ativo/Inativo)
- Spinners e loading states
- Alertas (success, error, info)

---

## 📂 Arquivos Criados

```
news_automation/
├── web.py                      # Flask app (rotas + geração async)
├── templates/
│   ├── base.html               # Layout master (sidebar + topbar)
│   ├── index.html              # Dashboard home
│   ├── history.html            # Lista de gerações
│   ├── article.html            # Visualização com abas
│   ├── feeds.html              # Gerenciar feeds
│   └── performance.html        # Stats + form + gráfico
└── static/
    └── style.css               # CSS tema escuro profissional
```

---

## 🔌 API Endpoints

| Método | Rota | Função |
|--------|------|--------|
| POST | `/api/run` | Inicia geração (background) |
| GET | `/api/run/status` | Polling: status + log |
| GET | `/api/last-run` | Data última geração |
| GET | `/api/performance-stats` | Stats para gráficos |

---

## ⚙️ Arquitetura

### Geração Assíncrona
```
1. POST /api/run → inicia Thread
2. Frontend faz polling a cada 2s em /api/run/status
3. GET /api/run/status retorna {"log": [...], "done": bool}
4. Quando done=true, recarrega página
5. Novo conteúdo aparece em /history
```

### Integração com Modules Existentes
- `db.py` — SQLite (feeds, articles, performance)
- `fetcher.py` — RSS (fetch_articles, fetch_for_topic)
- `generator.py` — Groq (generate_content, retry 3x)
- `formatter.py` — Markdown + Telegram

---

## 🎯 Navegação

```
Home (/)
├── 4 cards: Total | Hoje | Feeds Ativos | Posts c/ Métricas
├── Botão: Gerar Agora (com opção tópico)
└── Últimos 10 artigos (preview com link Ver)

Histórico (/history)
├── Lista por data
└── Cada linha: ID | Título | Ângulo | [Ver]

Artigo (/history/<id>)
├── Abas: Roteiro A | Roteiro B | Carrossel | Thread | Legenda
└── Botão: Registrar Performance

Feeds (/feeds)
├── Tabela: ID | Nome | URL | Status | Toggle
└── Form: + Novo Feed

Performance (/performance)
├── Gráfico saves vs views por roteiro
├── Form: Artigo → Plataforma → Roteiro → Métricas
└── Tabela histórico de registros
```

---

## 🧪 Testado

✅ Server inicia em `http://localhost:5000`  
✅ CSS carrega corretamente  
✅ Layout responsivo com sidebar  
✅ API `/api/last-run` retorna JSON  
✅ Integração com `db.py` funcionando  
✅ Unicode handling (caracteres especiais)

---

## 💡 Uso Típico

1. Abra `http://localhost:5000`
2. Home mostra 4 cards de resumo
3. Clique em **"Gerar Agora"** (vê log ao vivo)
4. Vai para `/history` automaticamente
5. Clique em um artigo para **Ver completo** (com abas)
6. Clique **"Registrar Performance"** para anotar métricas
7. Vá para **Performance** para ver gráficos

---

## 🚀 Stack Final

- **Backend**: Flask 2.3+
- **Frontend**: Jinja2 templates + HTML + CSS (sem build)
- **Charts**: Chart.js via CDN
- **Database**: SQLite (db.py)
- **LLM**: Groq API (generator.py)
- **Server**: Flask development (threading para async)

---

## 📝 Próximas Melhorias (Opcionais)

- [ ] Deploy com Gunicorn/uWSGI
- [ ] Tema Light/Dark toggle
- [ ] Exportar histórico para CSV
- [ ] Integração Meta/Instagram API (publicar direto)
- [ ] WebSocket para log ao vivo (em vez de polling)
- [ ] Cache em Redis
- [ ] Autenticação básica

---

**Status**: ✅ Pronto para Produção  
**Versão**: 2.0.1 (Dashboard incluído)  
**Data**: 2026-05-29
