# 🚀 Setup Completo — Railway Deploy em 5 Passos

## **PASSO 1: Criar Repositório GitHub** (1 min)

1. Abra: https://github.com/new
2. **Repository name**: `news-automation`
3. **Description**: `News Automation Dashboard v2.0`
4. Deixe **Public** (para Railway conseguir acessar)
5. **NÃO** selecione "Initialize with README"
6. Clique em **"Create repository"**

Você verá esta tela:
```
Quick setup — if you've done this kind of thing before

...or push an existing repository from the command line

git remote add origin https://github.com/SEU_USUARIO/news-automation.git
git branch -M main
git push -u origin main
```

**Copie a URL:** `https://github.com/SEU_USUARIO/news-automation.git`

---

## **PASSO 2: Executar Script de Setup** (2 min)

Abra PowerShell **na pasta do projeto**:

```powershell
cd C:\Users\Admin\news_automation
.\setup_railway.ps1
```

O script vai:
1. Pedir a URL do seu repositório GitHub
2. Cole: `https://github.com/SEU_USUARIO/news-automation.git`
3. Fazer push automático do código
4. Mostrar as próximas instruções

Se pedir senha/token:
- Vá para: https://github.com/settings/tokens
- Clique em **"Generate new token"**
- Escopo: ✅ repo
- Copie o token
- Cole no PowerShell como senha

---

## **PASSO 3: Conectar Railway** (2 min)

1. Abra: https://railway.app
2. Faça **login** (pode usar GitHub — recomendado)
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub Repo"**
5. Procure por **"news-automation"**
6. Clique em **"Deploy Now"**

Railway começará a fazer deploy automaticamente. Você verá um log com mensagens tipo:
```
Building...
Installing dependencies...
Running gunicorn...
Deployment successful! ✓
```

Aguarde **2-3 minutos** até aparecer ✅.

---

## **PASSO 4: Adicionar Volume** (1 min)

O Volume permite que o banco de dados persista entre deploys.

1. No projeto Railway → **"Storage"** (lado esquerdo)
2. Clique em **"Create Volume"** ou **"Add Storage"**
3. **Mount Path**: `/data`
4. Tamanho: deixe padrão (1 GB)
5. Clique em **"Create"**

---

## **PASSO 5: Configurar Variáveis de Ambiente** (2 min)

Railway precisa de suas credenciais do Groq e Telegram.

1. No projeto Railway → **"Variables"** (lado esquerdo)
2. Para cada variável abaixo, clique em **"Add Variable"**:

### Variável 1: GROQ_API_KEY
- **Nome**: `GROQ_API_KEY`
- **Valor**: Copie de `.env` local (linha: `GROQ_API_KEY=gsk_...`)
- Clique em **"Add"**

### Variável 2: TELEGRAM_BOT_TOKEN
- **Nome**: `TELEGRAM_BOT_TOKEN`
- **Valor**: Copie de `.env` local (linha: `TELEGRAM_BOT_TOKEN=8929995721:AAHA58dx...`)
- Clique em **"Add"**

### Variável 3: TELEGRAM_CHAT_ID
- **Nome**: `TELEGRAM_CHAT_ID`
- **Valor**: Copie de `.env` local (linha: `TELEGRAM_CHAT_ID=5690186897`)
- Clique em **"Add"**

### Variável 4: DATABASE_PATH
- **Nome**: `DATABASE_PATH`
- **Valor**: `/data/data.db`
- Clique em **"Add"**

✅ **Todas as 4 variáveis adicionadas!**

---

## **PRONTO! 🎉**

Seu dashboard está online!

### Encontrar sua URL:

1. No projeto Railway → **"Domains"**
2. Você verá uma URL tipo:
   ```
   https://news-automation-production.up.railway.app
   ```
3. Clique nela para abrir seu dashboard!

---

## 🎯 Seu Dashboard Online Tem:

```
✅ Home               — Cards de resumo + Botão Gerar
✅ Histórico          — Ver artigos (banco persistente!)
✅ Feeds             — Gerenciar RSS
✅ Performance       — Rastrear métricas
✅ Automação Telegram — Continua funcionando 24/7
```

---

## 📝 Notas Importantes

### **Banco de Dados**
- Local: `data.db` em sua máquina (não sobe para GitHub)
- Railway: `/data/data.db` (persiste no Volume)
- **Eles são independentes!** Railway começa com banco vazio.

### **Fazer Mudanças**
Sempre que editar o código:
```powershell
git add .
git commit -m "Sua mensagem aqui"
git push origin main
```

Railway fará deploy automaticamente! Sem precisa fazer mais nada.

### **Automação Telegram**
A automação local (Task Scheduler) continua funcionando normalmente. Railway é só para o dashboard.

---

## 🆘 Se Algo Der Errado

### **"Deployment failed"**
- Clique no deployment no Railway → "Logs"
- Procure pela mensagem de erro
- Verifique se todas as variáveis estão corretas

### **"Connection refused" na URL**
- Railway pode estar reiniciando
- Aguarde 30 segundos e recarregue

### **Banco de dados vazio**
- Normal! Use o botão "Gerar Agora" no dashboard para gerar conteúdo

### **Telegram não funciona**
- Verifique se GROQ_API_KEY, TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID estão corretos nas Variables do Railway

---

## ✨ Resultado Final

```
Local Machine:
  ✅ CLI: python main.py run
  ✅ Automação: Task Scheduler → Telegram
  ✅ Dashboard: python web.py (localhost:5000)

Railway (Online):
  ✅ Dashboard: 24/7 em https://seu-app.railway.app
  ✅ Banco: Persistente no Volume
  ✅ Custo: Grátis!
```

---

## 📞 Resumo dos Comandos

```powershell
# 1. Criar repo em https://github.com/new
# 2. Executar script
cd C:\Users\Admin\news_automation
.\setup_railway.ps1

# 3. Entrar em https://railway.app
# 4. Deploy from GitHub Repo
# 5. Add Volume + Variables
# 6. Acessar sua URL!
```

---

**Tempo total: ~10 minutos**  
**Status: Pronto para ir online!** 🚀
