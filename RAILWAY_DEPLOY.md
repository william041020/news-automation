# 🚀 Guia de Deploy no Railway — News Automation

## ✅ Arquivos de Deploy Criados

```
✅ Procfile              — Comando de startup para Railway
✅ runtime.txt          — Define Python 3.11.9
✅ .gitignore           — Protege .env e dados locais
✅ requirements.txt     — Inclui gunicorn para produção
✅ web.py               — Lê porta do ambiente ($PORT)
✅ db.py                — Lê caminho do BD ($DATABASE_PATH)
✅ .git/                — Repositório git inicializado
```

---

## 📋 Passo a Passo para Deploy

### **Passo 1: Criar Conta no Railway** (2 min)

1. Acesse: https://railway.app
2. Clique em **"Sign Up"**
3. Use sua conta **GitHub** (recomendado) ou email
4. Confirme seu email

---

### **Passo 2: Criar Repositório no GitHub** (3 min)

1. Vá para: https://github.com/new
2. **Repository name**: `news-automation`
3. **Description**: `News Automation Dashboard v2.0`
4. **Public** ou **Private** (sua escolha)
5. NÃO selecione "Initialize with README" (vamos fazer push local)
6. Clique em **"Create repository"**

Você verá uma URL assim: `https://github.com/SEU_USUARIO/news-automation.git`

---

### **Passo 3: Fazer Push para GitHub** (2 min)

No PowerShell, na pasta do projeto:

```powershell
cd C:\Users\Admin\news_automation

# Adicionar o repositório remoto
git remote add origin https://github.com/SEU_USUARIO/news-automation.git

# Fazer push da branch main
git branch -M main
git push -u origin main
```

Você verá:
```
Enumerating objects: 29, done.
Counting objects: 100% (29/29), done.
...
* [new branch]      main -> main
```

✅ **Pronto! Seu código está no GitHub.**

---

### **Passo 4: Conectar Railway ao GitHub** (2 min)

1. Volte ao **Railway Dashboard**: https://railway.app/dashboard
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub Repo"**
4. Clique em **"Authorize Railway"** (se for a primeira vez)
5. Selecione sua conta GitHub
6. Procure por **`news-automation`** e clique nele
7. Clique em **"Deploy Now"**

Railway começará a fazer deploy automaticamente!

✅ **Você verá um log de deploy em tempo real:**
```
[12:34:56] Building...
[12:34:58] Installing dependencies
[12:35:10] Running gunicorn...
[12:35:15] Deployment successful
```

---

### **Passo 5: Adicionar Volume (Persistência SQLite)** (3 min)

Para que o banco de dados persista entre deploys:

1. No **Railway Dashboard** → clique no seu projeto **"news-automation"**
2. Vá para **"Storage"** (lado esquerdo)
3. Clique em **"Create Volume"**
4. **Mount Path**: `/data`
5. Deixe o tamanho padrão (1 GB)
6. Clique em **"Create"**

✅ **Seu banco agora persiste!**

---

### **Passo 6: Configurar Variáveis de Ambiente** (3 min)

1. No projeto Railway → **"Variables"** (lado esquerdo)
2. Clique em **"New Variable"**
3. Adicione **4 variáveis**:

| Variável | Valor |
|----------|-------|
| `GROQ_API_KEY` | `gsk_xxxxxxxxxxxxxxxx` (da .env local) |
| `TELEGRAM_BOT_TOKEN` | `8929995721:AAHA58dxB_IV...` (da .env) |
| `TELEGRAM_CHAT_ID` | `5690186897` (da .env) |
| `DATABASE_PATH` | `/data/data.db` |

4. Para cada uma:
   - Digite a variável
   - Clique em **"Add"**

✅ **Variáveis configuradas!**

---

### **Passo 7: Acessar seu Dashboard** (1 min)

Pronto! Railway gerou automaticamente uma URL para seu app.

1. No projeto Railway → **"Deployment"**
2. Procure por **"Domains"**
3. Você verá uma URL tipo: `https://news-automation-production.up.railway.app`
4. Clique nela para abrir!

🎉 **Seu dashboard está online!**

---

## 🎯 Seu Dashboard agora tem:

```
✅ Home                 — Cards de resumo + Botão Gerar
✅ Histórico            — Ver artigos gerados (BD online)
✅ Feeds               — Gerenciar feeds
✅ Performance         — Rastrear métricas
✅ Automação Telegram  — Continua funcionando 24/7
✅ Banco de Dados      — SQLite persistente no Volume
```

---

## 🔄 Workflow Contínuo

Agora, sempre que você fizer uma mudança:

```powershell
# 1. Editar o código
# (exemplo: editar web.py)

# 2. Fazer commit
git add .
git commit -m "Atualizacao: sua mudança aqui"

# 3. Fazer push
git push origin main

# 4. Railway faz deploy automaticamente!
# Você verá o log no Railway Dashboard
```

**Não precisa fazer mais nada — Railway detecta o push e redeploy!**

---

## 🧪 Testar Localmente (Opcional)

Antes de fazer push, pode testar localmente:

```powershell
# Instalar gunicorn
python -m pip install gunicorn

# Rodar com a mesma config de produção
$env:PORT = "5000"
$env:DATABASE_PATH = "data.db"
gunicorn web:app --bind 0.0.0.0:5000 --workers 1 --timeout 120
```

Acesse: http://localhost:5000

---

## 📊 Dashboard Online vs Local

| Aspecto | Local | Railway |
|---------|-------|---------|
| **URL** | localhost:5000 | seu-app.railway.app |
| **Banco de dados** | `data.db` local | `/data/data.db` (Volume) |
| **Disponibilidade** | Só quando web.py roda | 24/7 |
| **Automação** | Manual ou Task Scheduler | Continuam automáticas |
| **Custo** | Grátis | Grátis (tier inicial) |

---

## 💰 Preços Railway

```
Tier Gratuito:
  • $5/mês em créditos
  • Suficiente para este projeto
  • 1 GB Volume Storage incluído

Depois dos $5 iniciais:
  • Você decide quanto gastar
  • Pode pausar qualquer hora
  • Não há contrato
```

---

## 🆘 Troubleshooting

### **"Deployment failed"**
Procure no log (Railway Dashboard → Deployments):
- Se for erro de PORT: já está corrigido (lê `$PORT`)
- Se for erro de importação: verifique `requirements.txt`
- Se for erro de BD: certifique-se que o Volume está em `/data`

### **"Connection refused"**
Railway pode estar reiniciando. Aguarde 30 segundos e recarregue.

### **"Database is empty"**
Normal! Railway começa com BD vazio. Gere conteúdo pelo botão no dashboard.

### **"Telegram não envia"**
Verifique variáveis de ambiente (GROQ_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID).

---

## 📞 Resumo Final

```
✅ Arquivos criados e commitados
✅ Git repository inicializado
✅ Pronto para fazer push para GitHub
✅ Railway fará deploy automaticamente

Próximo passo: Criar repo no GitHub e conectar Railway
```

**Qualquer dúvida durante o deploy, avise!** 🚀

---

**Data**: 2026-05-29  
**Status**: ✅ Pronto para Deploy  
**Tempo para Online**: ~5 minutos
