# 🚀 GUIA COMPLETO - Deploy no Streamlit Cloud

## 📱 Links Rápidos

- **Streamlit Cloud**: https://share.streamlit.io/
- **Seu Repositório GitHub**: https://github.com/hcarquejaufpr/robo-investimentos
- **Commit Atual**: `7685050` - Estado estável da aplicação

---

## ✅ CHECKLIST PRÉ-DEPLOY

### 1️⃣ Arquivos Prontos
- [x] `main.py` - Aplicação principal
- [x] `requirements.txt` - Dependências Python
- [x] `database.py` - Banco de dados SQLite
- [x] `config.py` - Configurações
- [x] `backup_manager.py` - Backup Google Sheets (opcional)
- [x] `analise_bitcoin.py` - Análise de Bitcoin
- [x] `.streamlit/config.toml` - Configurações visuais
- [x] `.streamlit/secrets.toml` - NUNCA commitado (apenas local)

### 2️⃣ Dependências Verificadas
```txt
✅ yfinance     - Dados de mercado
✅ pandas       - Manipulação de dados
✅ numpy        - Cálculos numéricos
✅ streamlit    - Framework web
✅ plotly       - Gráficos interativos
✅ gspread      - Google Sheets (backup)
✅ google-auth  - Autenticação Google
✅ requests     - HTTP requests
```

---

## 🎯 PASSO A PASSO - DEPLOY

### PASSO 1: Acessar Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta Google/GitHub
3. Clique em **"New app"** (botão superior direito)

### PASSO 2: Configurar Deploy

**Preencha os campos:**

```
Repository:        hcarquejaufpr/robo-investimentos
Branch:            main
Main file path:    main.py
App URL (optional): robo-investimentos (ou deixe em branco)
```

**Configurações Avançadas** (clique em "Advanced settings"):
```
Python version:     3.12
```

### PASSO 3: Configurar Secrets (CRÍTICO!)

**ANTES de clicar em "Deploy"**, clique em **"Advanced settings" > "Secrets"**

Cole o seguinte template e preencha com seus dados:

```toml
# ============================================================================
# EMAIL - NOTIFICAÇÕES
# ============================================================================
# Obrigatório para enviar alertas de Stop Loss, Stop Gain, etc.
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_app_google"

# ⚠️ IMPORTANTE: Use "Senha de App" do Google, não sua senha normal!
# Como criar: https://myaccount.google.com/apppasswords
# 1. Acesse o link acima
# 2. Clique em "Criar senha de app"
# 3. Escolha "App: Mail" e "Dispositivo: Outro"
# 4. Digite "Robo Investimentos" e clique em "Gerar"
# 5. Copie a senha de 16 caracteres (sem espaços)


# ============================================================================
# GOOGLE SHEETS BACKUP (OPCIONAL)
# ============================================================================
# Só necessário se você quiser backup automático no Google Sheets

[gcp_service_account]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "seu-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_PRIVADA_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "seu-service-account@seu-projeto.iam.gserviceaccount.com"
client_id = "seu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/seu-email"

# 📝 Como obter estas credenciais:
# 1. Google Cloud Console: https://console.cloud.google.com/
# 2. Crie um projeto novo (ou use existente)
# 3. Ative: "Google Sheets API" e "Google Drive API"
# 4. Crie Service Account: IAM & Admin > Service Accounts > Create
# 5. Baixe o JSON: Actions > Manage Keys > Add Key > JSON
# 6. Copie TODO o conteúdo do JSON aqui (formato TOML)
# 7. Compartilhe a planilha com o email do service account

backup_sheet_name = "RoboInvestimentos_Backup"
```

### PASSO 4: Deploy! 🚀

1. Após configurar os secrets, clique em **"Deploy!"**
2. Aguarde 5-10 minutos (primeira vez é mais lenta)
3. O Streamlit vai:
   - ✅ Clonar seu repositório
   - ✅ Instalar todas as dependências
   - ✅ Executar `main.py`
   - ✅ Gerar URL pública

---

## 🔐 CONFIGURAÇÃO MÍNIMA (Sem Backup Google Sheets)

Se você **não quiser** usar backup no Google Sheets, use apenas:

```toml
# EMAIL - NOTIFICAÇÕES APENAS
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_app_google"
```

✅ **VANTAGEM**: Mais simples, menos configuração  
⚠️ **DESVANTAGEM**: Sem backup automático, dados apenas em SQLite

---

## 📊 FUNCIONALIDADES DA APLICAÇÃO

### 🔹 Gestão de Carteira
- ✅ Ações Americanas (AAPL, TSLA, NVDA, etc.)
- ✅ FIIs Brasileiros (HGLG11, KNIP11, etc.)
- ✅ Tesouro Direto (Selic, IPCA+, Prefixado)
- ✅ Bitcoin (BTC-USD) com análise técnica

### 🔹 Análise Técnica
- ✅ Stop Loss & Stop Gain automáticos
- ✅ RSI, MACD, Médias Móveis
- ✅ Bandas de Bollinger
- ✅ Recomendações de compra/venda

### 🔹 Notificações
- ✅ Alertas por email quando ativos batem stops
- ✅ Relatórios diários (via GitHub Actions)

### 🔹 Backup & Recuperação
- ✅ Backup automático no Google Sheets (opcional)
- ✅ Recuperação de dados em caso de reset
- ✅ Banco SQLite persistente

---

## 🐛 TROUBLESHOOTING

### ❌ ERRO: "ModuleNotFoundError"
**Solução**: Verifique se `requirements.txt` está correto
```bash
git add requirements.txt
git commit -m "fix: Corrige requirements.txt"
git push
```

### ❌ ERRO: Email não enviando
**Causas comuns**:
1. EMAIL_PASSWORD não é senha de app do Google
2. EMAIL_SENDER não matcheia a conta do PASSWORD
3. 2FA não está ativado no Google

**Solução**: Crie senha de app em https://myaccount.google.com/apppasswords

### ❌ ERRO: "gcp_service_account not found"
**Isso é OK!** Se você não configurou Google Sheets backup, a aplicação funciona normalmente usando apenas SQLite. O erro aparece mas não impede o funcionamento.

**Solução** (se quiser remover o erro):
- Configure `[gcp_service_account]` nos secrets, OU
- Ignore (não afeta funcionalidade principal)

### ❌ App reinicia e perde dados
**Causa**: Streamlit Community tier reinicia apps inativos (sem armazenamento persistente)

**Soluções**:
1. **Configure backup Google Sheets** (recomendado)
2. Use Streamlit Cloud Teams ($20/mês - persistência garantida)
3. Faça backups manuais periodicamente

---

## 🎨 PERSONALIZAÇÃO

### Mudar cores/tema

Edite `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"        # Cor principal
backgroundColor = "#0E1117"      # Fundo
secondaryBackgroundColor = "#262730"  # Cards
textColor = "#FAFAFA"            # Texto
```

### Adicionar ativos

Edite `config.py`:

```python
US_STOCKS = ['AAPL', 'MSFT', 'GOOGL', ...]
BR_FIIS = ['HGLG11.SA', 'MXRF11.SA', ...]
```

Commit e push:
```bash
git add config.py
git commit -m "feat: Adiciona novos ativos"
git push
```

Streamlit auto-deploy em ~2 minutos.

---

## 📞 SUPORTE

### Logs do Streamlit Cloud
1. Acesse seu app no Streamlit Cloud dashboard
2. Clique nos 3 pontos > "Logs"
3. Verifique erros em vermelho

### Testar localmente antes de deploy
```bash
streamlit run main.py
```

Acesse: http://localhost:8501

---

## ✅ CHECKLIST FINAL

Antes de fazer deploy, confirme:

- [ ] `requirements.txt` está no repositório
- [ ] Commit `7685050` está no GitHub
- [ ] EMAIL_SENDER configurado nos secrets
- [ ] EMAIL_PASSWORD (senha de app) configurado
- [ ] [OPCIONAL] gcp_service_account configurado se quiser backup

---

## 🚀 COMANDOS ÚTEIS

```bash
# Ver commit atual
git log --oneline -n 5

# Forçar push (se necessário)
git push --force origin main

# Ver status
git status

# Adicionar tudo e commitar
git add .
git commit -m "deploy: Preparando para Streamlit Cloud"
git push
```

---

**Criado em:** 06/02/2026  
**Commit base:** 7685050  
**Versão:** Robô de Investimentos v1.0

