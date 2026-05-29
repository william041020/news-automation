# 📋 Comandos Copy & Paste — Deploy Railway

## ⚡ Quick Start (Copie e Cole)

Siga esses passos na ordem:

---

## **PASSO 1: Criar GitHub Repository**

Abra em seu navegador:
```
https://github.com/new
```

Preencha:
- **Repository name**: `news-automation`
- **Description**: `News Automation Dashboard v2.0`
- **Visibility**: Public
- NÃO marque "Initialize this repository with"

Clique em **"Create repository"**

---

## **PASSO 2: Copiar URL do Seu Repositório**

Após criar, você verá:
```
Quick setup — if you've done this kind of thing before

...or push an existing repository from the command line

git remote add origin https://github.com/SEU_USUARIO/news-automation.git
```

**Copie a URL:**
```
https://github.com/SEU_USUARIO/news-automation.git
```

(Troque `SEU_USUARIO` pelo seu nome de usuário GitHub)

---

## **PASSO 3: Abra PowerShell na Pasta do Projeto**

```powershell
cd C:\Users\Admin\news_automation
```

---

## **PASSO 4: Execute Esses Comandos (um de cada vez)**

### Comando 1:
```powershell
git remote add origin https://github.com/SEU_USUARIO/news-automation.git
```

### Comando 2:
```powershell
git branch -M main
```

### Comando 3:
```powershell
git push -u origin main
```

Quando pedir **"Username"**: seu nome de usuário GitHub  
Quando pedir **"Password"**: seu token do GitHub (veja abaixo)

---

## **PASSO 5: Gerar Token GitHub** (se pedir autenticação)

Se você vir:
```
Username for 'https://github.com': 
Password for 'https://seu_usuario@github.com': 
```

Significa que precisa de um token. Faça isso:

1. Abra: https://github.com/settings/tokens
2. Clique em **"Generate new token"**
3. **Token name**: `railway-deploy`
4. **Expiration**: 90 days
5. **Select scopes**: marque ✅ `repo`
6. Clique em **"Generate token"**
7. **COPIE O TOKEN** (não vão mostrar de novo!)
8. Cole no PowerShell como "Password"

---

## **PASSO 6: Confirmar que o Push Funcionou**

Você verá:
```
Enumerating objects: 29, done.
Counting objects: 100% (29/29), done.
...
* [new branch]      main -> main
```

✅ **Sucesso! Seu código está no GitHub!**

---

## **PASSO 7: Conectar Railway**

1. Abra: https://railway.app
2. Faça login (pode usar GitHub)
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub Repo"**
5. Procure por `news-automation`
6. Clique nele
7. Clique em **"Deploy Now"**

Railway começará o deploy. Aguarde 2-3 minutos. Você verá um log tipo:
```
Building...
Installing dependencies...
Running gunicorn...
✓ Deployment successful!
```

---

## **PASSO 8: Adicionar Volume** (persistência do banco)

1. No projeto Railway → **"Storage"** (lado esquerdo)
2. Clique em **"+ Create Volume"** ou **"Add Storage"**
3. **Mount Path**: `/data`
4. Clique em **"Create"**

---

## **PASSO 9: Adicionar Variáveis de Ambiente**

1. No projeto Railway → **"Variables"**
2. Para cada uma, clique em **"Add Variable"**:

### Variável 1:
```
Name: GROQ_API_KEY
Value: gsk_xxxxxxx... (copie de sua .env local)
```

### Variável 2:
```
Name: TELEGRAM_BOT_TOKEN
Value: 8929995721:AAHA58dx... (copie de sua .env local)
```

### Variável 3:
```
Name: TELEGRAM_CHAT_ID
Value: 5690186897 (copie de sua .env local)
```

### Variável 4:
```
Name: DATABASE_PATH
Value: /data/data.db
```

---

## **PASSO 10: Acessar seu Dashboard!**

1. No projeto Railway → **"Deployments"**
2. Procure por **"Domains"**
3. Você verá uma URL tipo:
   ```
   https://news-automation-production.up.railway.app
   ```
4. Clique para abrir!

🎉 **Seu dashboard está online!**

---

## 📝 Comandos Úteis Depois

### Ver status do git:
```powershell
git status
```

### Fazer mudanças:
```powershell
git add .
git commit -m "Sua mensagem"
git push origin main
```

Railway faz deploy automaticamente!

---

## 🆘 Se Algo Der Errado

### "fatal: 'origin' does not appear to be a git repository"
→ Você está na pasta certa? `cd C:\Users\Admin\news_automation`

### "fatal: Could not read from remote repository"
→ Você usou a URL correta? Troque `SEU_USUARIO` pela seu nome real.

### "invalid username or password"
→ Use um token GitHub, não sua senha. Gere em: https://github.com/settings/tokens

### "Deployment failed" no Railway
→ Clique em "Logs" para ver o erro detalhado. Verifique as Variables.

---

## ✨ Resumo dos 10 Passos

```
1. ✅ Criar GitHub repo (https://github.com/new)
2. ✅ Copiar URL
3. ✅ Abrir PowerShell na pasta
4. ✅ git remote add origin URL
5. ✅ git branch -M main
6. ✅ git push -u origin main
7. ✅ Conectar Railway (railway.app)
8. ✅ Add Volume (/data)
9. ✅ Add Variables (4 variáveis)
10. ✅ Acessar sua URL!

TOTAL: ~15 minutos
```

---

**Pronto? Comece pelo PASSO 1!** 🚀
