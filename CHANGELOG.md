# Changelog — News Automation v2.0

## 📦 Novos Arquivos

- ✅ `db.py` — Camada SQLite com schema completo
- ✅ `fetcher.py` — Busca RSS dinâmica + busca por tópico
- ✅ `generator.py` — Geração com retry + formato Thread
- ✅ `formatter.py` — Formatação Markdown + Telegram
- ✅ `notifier.py` — Envio Telegram isolado
- ✅ `__init__.py` — Package initialization
- ✅ `__main__.py` — Entry point para `python -m`
- ✅ `IMPLEMENTACAO.md` — Documentação técnica
- ✅ `GUIA_RAPIDO.md` — Quick start guide
- ✅ `CHANGELOG.md` — Este arquivo

## 🔄 Arquivos Modificados

### `main.py`
- ❌ Removido: lógica monolítica (1 arquivo com ~380 linhas)
- ✅ Adicionado: CLI estruturado com Click (~350 linhas)
- ✅ Novo: 6 grupos de comandos (run, feeds, history, perf)
- ✅ Novo: Função `safe_echo()` para Unicode
- ✅ Melhorado: Help automático em cada comando

### `setup_scheduler.ps1`
- ✅ Atualizado: Chama `python main.py run` em vez de `python main.py`
- ✅ Novo: Parâmetro `-ComTelegram` para envio automático
- ✅ Novo: Help estendido com comandos CLI
- ✅ Novo: Mostra modo Telegram configurado

### `requirements.txt`
- ✅ Adicionado: `click>=8.1.0`

## 🎯 Novas Funcionalidades

### CLI Interativo

#### Comando `run`
```bash
python main.py run                              # Feeds do banco
python main.py run --topic "AI Marketing"       # Tópico customizado
python main.py run --no-telegram                # Sem enviar
```

#### Comando `feeds`
```bash
python main.py feeds list      # Listar feeds
python main.py feeds add <url> <nome>   # Adicionar
python main.py feeds remove <id>        # Desativar
python main.py feeds enable <id>        # Ativar
```

#### Comando `history`
```bash
python main.py history list             # Últimas 10 gerações
python main.py history show <id>        # Conteúdo completo
```

#### Comando `perf`
```bash
python main.py perf log                 # Registrar métricas (wizard)
python main.py perf stats               # Análise agregada
```

### Banco de Dados

```sql
CREATE TABLE feeds (
    id, url, name, active, created_at
);

CREATE TABLE articles (
    id, run_date, title, source, link, summary,
    content_json, gancho_tema, created_at
);

CREATE TABLE performance (
    id, article_id, platform, roteiro,
    views, saves, likes, comments, posted_at, logged_at
);
```

**Benefícios:**
- Histórico persistente
- Feeds gerenciáveis via CLI
- Base para análise de performance

### Novo Formato: Thread

Adicionado ao JSON gerado:
```json
"thread": {
    "post_1": "Gancho para X/LinkedIn",
    "post_2": "Contexto",
    ...
    "post_8": "CTA"
}
```

Incluído automaticamente no Markdown e preview Telegram.

### Melhorias na Geração

- ✅ Retry automático (3x) com exponential backoff
- ✅ Validação de schema JSON antes de salvar
- ✅ Suporte a tópicos customizados via Google News RSS
- ✅ Tratamento de Unicode (Windows console)

## 📊 Métricas de Código

| Métrica | v1.0 | v2.0 | Mudança |
|---------|------|------|---------|
| Arquivos | 1 | 10+ | +900% |
| Linhas (principal) | 380 | 350 | -8% (melhor organizado) |
| Funcionalidades | 1 | 15+ | +1400% |
| Testes manuais | Manual | 7 comandos | Automático |

## 🔍 Testes Realizados

- ✅ CLI help (todos os comandos)
- ✅ `feeds list` — 6 feeds carregados
- ✅ `feeds add/remove/enable`
- ✅ `run` com feeds padrão — 3 artigos gerados
- ✅ `run --topic "..."` — busca customizada funcionando
- ✅ `history list` — mostra 6 artigos de 2 runs
- ✅ `history show 1` — conteúdo completo com Thread
- ✅ `perf stats` — sem dados (estrutura OK)
- ✅ Thread format — incluído em Markdown + Telegram
- ✅ Unicode handling — caracteres especiais OK

## 🚀 Próximos Passos (Opcionais)

- [ ] Integração Meta API (Instagram/Reels)
- [ ] Integração LinkedIn API
- [ ] Dashboard Web (Flask)
- [ ] Docker container
- [ ] Tests automatizados (pytest)
- [ ] GitHub Actions CI/CD

## 📝 Breaking Changes

- ❌ Task Scheduler **precisa** ser reconfigurado
  - Antigo: `python main.py`
  - Novo: `python main.py run [--no-telegram]`
  
  **Solução:** Execute `.\setup_scheduler.ps1` novamente

---

**Versão:** 2.0  
**Data:** 2026-05-29  
**Status:** ✅ Pronto para produção
