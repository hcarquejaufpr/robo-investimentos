# 🚀 Deploy no Streamlit Community Cloud

## 📋 Pré-requisitos

1. ✅ Conta no GitHub
2. ✅ Conta no Streamlit Community Cloud (https://streamlit.io/cloud)
3. ✅ Repositório atualizado com as funcionalidades mais recentes

## 🎉 Últimas Funcionalidades Implementadas

### ₿ Análise de Bitcoin (v2.0)
- Análise técnica completa com RSI, MACD, Médias Móveis e Bandas de Bollinger
- Sistema de score e recomendação automática (compra/venda)
- Gráfico interativo com candlesticks
- Sinais de trading em tempo real

### 📊 Backup no Google Sheets
- Backup automático de carteiras no Google Sheets
- Recuperação de dados em caso de reset
- Sincronização bidirecional

## 🔧 Deploy Passo a Passo

### 1. Verificar Repositório GitHub

```bash
# Verificar status
git status

# Últimas alterações já foram enviadas
git log --oneline -5
```

**✅ Commit mais recente:**
```
feat: Adiciona backup Google Sheets e análise Bitcoin
- Sistema de backup automático no Google Sheets
- Análise técnica completa de Bitcoin (BTC-USD)
- Indicadores: RSI, MACD, Médias Móveis, Bandas Bollinger
- Sistema de score e recomendação (compra/venda)
- Gráfico interativo com candlesticks
```

### 2. Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Clique em **"New app"** (ou recarregue o existente)
3. Conecte sua conta do GitHub
4. Selecione:
   - Repository: `hcarquejaufpr/robo-investimentos`
   - Branch: `main`
   - Main file path: `main.py`
5. Clique em **"Deploy!"**

⏱️ **Tempo de deploy:** ~5-10 minutos

### 3. Configurar Secrets (OBRIGATÓRIO)

No painel do Streamlit Cloud:

1. Vá em **Settings > Secrets**
2. Adicione suas variáveis:

```toml
# Email para notificações
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_app_do_gmail"

# Google Sheets (OPCIONAL - apenas se usar backup)
# Cole aqui o conteúdo completo do arquivo gen-lang-client-*.json
# [GOOGLE_CREDENTIALS]
# type = "service_account"
# project_id = "seu-projeto"
# private_key_id = "..."
# private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
# client_email = "..."
# client_id = "..."
# auth_uri = "https://accounts.google.com/o/oauth2/auth"
# token_uri = "https://oauth2.googleapis.com/token"
# ...
```

## 📦 Arquivos Necessários

✅ `requirements.txt` - Dependências Python (inclui numpy para Bitcoin)  
✅ `main.py` - Arquivo principal do Streamlit  
✅ `database.py` - Módulo de banco de dados  
✅ `config.py` - Configurações da aplicação  
✅ `backup_manager.py` - Sistema de backup Google Sheets  
✅ `analise_bitcoin.py` - Módulo de análise de Bitcoin (NOVO)  
✅ `.streamlit/secrets.toml` - Credenciais (não commitado)  

## 🔗 Estrutura para Deploy

```
Robo_Investimentos/
├── main.py                      # Arquivo principal
├── config.py                    # Configurações
├── database.py                  # Banco de dados
├── backup_manager.py            # Backup Google Sheets
├── analise_bitcoin.py           # Análise Bitcoin (NOVO)
├── requirements.txt             # Dependências (atualizado com numpy)
├── ANALISE_BITCOIN.md          # Documentação Bitcoin (NOVO)
├── BACKUP_SISTEMA.md           # Documentação Backup (NOVO)
├── .streamlit/
│   └── secrets.toml            # Credenciais (criar manualmente no Streamlit Cloud)
└── data/                        # Criado automaticamente
    └── investimentos.db
```

## 🎯 Funcionalidades Implementadas

### 1. ₿ Análise de Bitcoin (Fevereiro 2026)
- ✅ Indicadores técnicos: RSI, MACD, Médias Móveis, Bandas de Bollinger
- ✅ Sistema de score (-100 a +100) e recomendação automática
- ✅ Gráfico interativo com candlesticks
- ✅ Análise de tendência e volume
- ✅ Sinais de trading em tempo real
- 📖 Documentação: [ANALISE_BITCOIN.md](ANALISE_BITCOIN.md)

### 2. 📊 Backup Google Sheets
- ✅ Backup automático de carteiras
- ✅ Recuperação de dados em caso de reset
- ✅ Sincronização bidirecional
- 📖 Documentação: [BACKUP_SISTEMA.md](BACKUP_SISTEMA.md)

### 3. 📈 Análise de Renda Variável
- ✅ Ações e ETFs americanos
- ✅ FIIs brasileiros
- ✅ Tesouro Direto
- ✅ Estratégias de saída personalizadas

## ⚙️ Requisitos Importantes

- O Streamlit Community Cloud tem **1GB de RAM**
- Limite de **1GB de armazenamento**
- ✅ **BACKUP AUTOMÁTICO CONFIGURADO**: Os dados agora persistem via Google Sheets!
- 📖 Veja [BACKUP_SISTEMA.md](BACKUP_SISTEMA.md) para instruções de configuração

## ⚠️ Problemas Conhecidos e Soluções

### 🔐 Certificado SSL no Bitcoin
Se houver problemas de SSL ao obter dados do Bitcoin:

1. **No Streamlit Cloud:** Geralmente funciona sem problemas
2. **Localmente:** Use variáveis de ambiente:
   ```powershell
   $env:PYTHONHTTPSVERIFY="0"
   $env:CURL_CA_BUNDLE=""
   streamlit run main.py
   ```

### 📊 Google Sheets Backup
Para ativar o backup no Google Sheets:

1. Crie um projeto no Google Cloud Console
2. Ative a Google Sheets API
3. Crie credenciais de conta de serviço
4. Compartilhe a planilha com o email da conta de serviço
5. Configure as credenciais no Streamlit Cloud Secrets

## 🌐 Após Deploy

Sua aplicação estará disponível em:
```
https://hcarqueja-robo-investimentos.streamlit.app
```

✅ **Deploy Automatizado:** Qualquer push para `main` atualiza automaticamente!

## 🔄 Verificações Pós-Deploy

1. ✅ Login funciona corretamente
2. ✅ Análise de Bitcoin carrega e exibe dados
3. ✅ Backup Google Sheets funciona (se configurado)
4. ✅ Ações e FIIs carregam normalmente
5. ✅ Gráficos são renderizados corretamente
6. ✅ Notificações por email funcionam (se configuradas)

## 📞 Troubleshooting

### Bitcoin não carrega
- Verifique conexão com Yahoo Finance
- SSL geralmente funciona no Streamlit Cloud
- Veja logs em "Manage app" > "Logs"

### Backup não funciona
- Verifique se credenciais estão corretas no Secrets
- Confirme que planilha está compartilhada com service account
- Verifique logs de erro

### Banco de dados reseta
- Configure backup Google Sheets
- Dados serão restaurados automaticamente no próximo login

## 🚀 Performance

- ⚡ Cache de 5 minutos para cotações
- 🔄 Refresh automático de dados
- 📊 Backup assíncrono (não bloqueia interface)

## 🎉 Pronto para Produção!

```bash
git add .
git commit -m "Atualização"
git push
```

## 🛠️ Troubleshooting

**App não inicia:**
- Verifique os logs no dashboard do Streamlit Cloud
- Confirme que `requirements.txt` está completo
- Certifique-se que `main.py` está no caminho correto

**Erro de dependências:**
- Adicione versões específicas no `requirements.txt`
- Exemplo: `streamlit==1.30.0`

**Banco de dados vazio após deploy:**
- ✅ **SOLUÇÃO IMPLEMENTADA**: Backup automático via Google Sheets
- 📖 Siga o guia: [CONFIGURAR_BACKUP_PERSISTENTE.md](CONFIGURAR_BACKUP_PERSISTENTE.md)
- Após configurado, os dados persistem automaticamente!

## 💡 Dicas

- Use `st.secrets` para acessar variáveis de ambiente
- Teste localmente antes do deploy: `streamlit run main.py`
- Configure limites de cache para economizar memória
- Use `@st.cache_data` para otimizar performance
