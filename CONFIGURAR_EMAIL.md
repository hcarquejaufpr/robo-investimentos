# 📧 GUIA RÁPIDO: Configurar Notificações por Email

## ✅ O que já está feito:
- ✅ Código de envio de email implementado
- ✅ Interface de configuração na sidebar
- ✅ Botão "Testar Notificação" funcionando
- ✅ Email da conta: casamentojuliaehenrique2017@gmail.com

## 🔧 O que VOCÊ precisa fazer:

### 📍 PASSO 1: Gerar Senha de App do Gmail

1. Acesse: https://myaccount.google.com/apppasswords
   - **Se não aparecer:** Você precisa ativar a verificação em 2 etapas primeiro
   
2. Ative a verificação em 2 etapas (se ainda não tiver):
   - Vá em: https://myaccount.google.com/security
   - Clique em "Verificação em duas etapas"
   - Siga as instruções (vai pedir seu celular)

3. Depois volte em: https://myaccount.google.com/apppasswords

4. Configure:
   - **App:** Selecione "E-mail"
   - **Dispositivo:** Selecione "Outro" e digite "Robô Investimentos"
   - Clique em **Gerar**

5. Copie a senha de 16 caracteres (formato: `xxxx xxxx xxxx xxxx`)

### 📍 PASSO 2: Configurar LOCALMENTE (para testar)

No arquivo: `.streamlit/secrets.toml` (já existe)

Substitua `COLE_AQUI_SUA_SENHA_DE_APP` pela senha que você copiou:

```toml
EMAIL_PASSWORD = "sua_senha_aqui_sem_espacos"
```

**Exemplo:**
```toml
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  ❌ ERRADO (com espaços)
EMAIL_PASSWORD = "abcdefghijklmnop"     ✅ CERTO (sem espaços)
```

### 📍 PASSO 3: Testar LOCALMENTE

1. No terminal PowerShell:
   ```powershell
   cd C:\RAG\Robo_Investimentos
   .\.venv\Scripts\Activate.ps1
   streamlit run main.py
   ```

2. No app Streamlit:
   - Na sidebar, expanda **"📧 Notificações Diárias"**
   - Marque **"Ativar notificações"**
   - Digite seu email: `hcarqueja@gmail.com` (ou outro)
   - Clique em **"💾 Salvar Configurações"**
   - Clique em **"🧪 Testar Notificação Agora"**

3. Verifique sua caixa de entrada!

### 📍 PASSO 4: Configurar no STREAMLIT CLOUD

1. Acesse: https://share.streamlit.io/

2. Encontre seu app: **robo-investimentos**

3. Clique em **⚙️ Settings** (canto superior direito)

4. Vá na aba **Secrets**

5. Cole este conteúdo (substituindo a senha):

```toml
password = "investidor2026"

EMAIL_SENDER = "casamentojuliaehenrique2017@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_16_caracteres_aqui"
```

6. Clique em **Save**

7. O app vai reiniciar automaticamente

### 📍 PASSO 5: Testar no Cloud

1. Acesse: https://robo-investimentos.streamlit.app

2. Faça login

3. Na sidebar, configure as notificações

4. Teste enviando um email

---

## 🎯 Resultado Esperado:

Você receberá um email formatado com:
- 🤖 **Cabeçalho:** Robô de Investimentos
- ⚠️ **Alertas:** Lista de ativos perto do stop ou alvo
- 📊 **Resumo:** Valor total, ganho potencial, perda potencial
- 🔗 **Link:** Para acessar o painel completo

---

## ⚠️ Possíveis Problemas:

### ❌ "Configure EMAIL_PASSWORD no secrets.toml"
- **Solução:** Você não configurou a senha no arquivo secrets.toml

### ❌ "Authentication failed"
- **Solução:** 
  1. Verifique se a senha está correta (sem espaços)
  2. Confirme que a verificação em 2 etapas está ativa
  3. Gere uma nova senha de app

### ❌ "Username and Password not accepted"
- **Solução:** 
  1. Certifique-se de usar uma "Senha de App", NÃO a senha normal do Gmail
  2. A conta precisa ter verificação em 2 etapas ativada

---

## 📱 Próximos Passos (Opcional):

### Envio Automático Diário

Para receber emails automáticos todos os dias às 9h, você pode:

1. **Usar GitHub Actions** (gratuito)
2. **Usar serviço como Zapier ou Make.com**
3. **Usar servidor próprio com cron job**

Se quiser implementar, me avise!

---

## 💡 Dicas:

- ✅ **Teste primeiro localmente** antes de configurar no Cloud
- ✅ **Use um email diferente** para receber (ex: hcarqueja@gmail.com)
- ✅ **Não compartilhe** a senha de app com ninguém
- ✅ **Revogue a senha** em https://myaccount.google.com/apppasswords se necessário

---

**Está tudo pronto! Agora é só seguir os passos acima.** 🚀
