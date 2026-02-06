# 📧 Guia de Configuração: Notificações Diárias Automáticas

## ✅ O que foi implementado?

Sistema de **notificações diárias automáticas** usando **GitHub Actions** (100% gratuito!):

- ✅ Roda todo dia no horário que você configurou (padrão: 09:00 BRT)
- ✅ Envia email com resumo da carteira
- ✅ Alertas de stop loss próximos
- ✅ Totalmente automático (não precisa acessar o app)

---

## 🔧 Configuração (15 minutos)

### **Passo 1: Configurar Secrets no GitHub**

1. **Acesse seu repositório no GitHub:**
   ```
   https://github.com/hcarquejaufpr/robo-investimentos
   ```

2. **Vá em:** `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

3. **Adicione os seguintes secrets:**

#### **Secret 1: GCP_SERVICE_ACCOUNT**
- **Name:** `GCP_SERVICE_ACCOUNT`
- **Value:** Conteúdo COMPLETO do arquivo `gen-lang-client-0919671346-30ffdbafba47.json`
  ```json
  {
    "type": "service_account",
    "project_id": "...",
    "private_key_id": "...",
    ...
  }
  ```

#### **Secret 2: SMTP_SERVER**
- **Name:** `SMTP_SERVER`
- **Value:** `smtp.gmail.com` (ou seu servidor SMTP)

#### **Secret 3: SMTP_PORT**
- **Name:** `SMTP_PORT`
- **Value:** `587`

#### **Secret 4: SMTP_USER**
- **Name:** `SMTP_USER`
- **Value:** Seu email completo (ex: `robo.investimentos.2025@gmail.com`)

#### **Secret 5: SMTP_PASSWORD**
- **Name:** `SMTP_PASSWORD`
- **Value:** **Senha de app do Gmail** (NÃO use a senha normal!)

---

### **Passo 2: Criar Senha de App do Gmail**

1. Acesse: https://myaccount.google.com/apppasswords
2. **Nome do app:** "Robo Investimentos GitHub"
3. Clique em **"Criar"**
4. **Copie a senha gerada** (16 caracteres)
5. Use essa senha no secret `SMTP_PASSWORD`

---

### **Passo 3: Fazer Deploy**

Execute no terminal:

```powershell
cd c:\RAG\Robo_Investimentos
git add .github send_daily_notifications.py
git commit -m "Adicionar sistema de notificações diárias automáticas via GitHub Actions"
git push origin main
```

---

### **Passo 4: Testar Manualmente**

1. **Acesse:** `https://github.com/hcarquejaufpr/robo-investimentos/actions`

2. **Clique em:** "Enviar Notificações Diárias" (workflow na lista)

3. **Clique em:** `Run workflow` → `Run workflow`

4. **Aguarde 2-3 minutos** e verifique seu email!

---

## ⏰ Configurar Horário

Por padrão, roda **09:00 BRT** (12:00 UTC).

**Para mudar o horário:**

1. Edite o arquivo: `.github/workflows/daily-notifications.yml`

2. Na linha do `cron`, ajuste:
   ```yaml
   # Formato: 'minuto hora * * *' (UTC)
   - cron: '0 12 * * *'  # 09:00 BRT
   ```

3. **Exemplos:**
   - `'0 13 * * *'` → 10:00 BRT
   - `'30 11 * * *'` → 08:30 BRT
   - `'0 21 * * *'` → 18:00 BRT

4. **Importante:** Horário é em **UTC** (BRT = UTC-3)

---

## 📊 O que o email contém?

✅ **Resumo da Carteira:**
- Valor total
- Ganhos
- Perdas

⚠️ **Alertas:**
- Ativos próximos do stop loss (<5%)
- Avisos importantes

🔗 **Link direto** para o painel completo

---

## 🐛 Troubleshooting

### ❌ "Email não enviado"

**Verifique:**
1. Secrets configurados corretamente no GitHub
2. Senha de app do Gmail (não senha normal!)
3. Notificações ativadas no app Streamlit
4. Email configurado nas notificações

### ❌ "Workflow falhou"

1. Vá em: `https://github.com/hcarquejaufpr/robo-investimentos/actions`
2. Clique no workflow que falhou
3. Veja os logs para identificar o erro
4. Corrija e rode manualmente de novo

### ⏰ "Não recebo no horário certo"

- GitHub Actions pode ter **delay** de até 15 minutos
- Horário é em **UTC**, não BRT
- Converta: BRT + 3 horas = UTC

---

## 💡 Dicas

✅ **Teste primeiro:** Use `Run workflow` manualmente antes de esperar o agendamento

✅ **Múltiplos horários:** Duplique a linha do `cron` no YAML

✅ **Desativar temporariamente:** Comente a linha do `cron` com `#`

---

## 🎉 Pronto!

Agora você receberá **emails automáticos** todo dia no horário configurado! 📧

**Sem custo, sem servidor, 100% automático!** 🚀
