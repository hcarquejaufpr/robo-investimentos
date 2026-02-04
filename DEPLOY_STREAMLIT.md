# 🚀 Deploy no Streamlit Community Cloud

## 📋 Pré-requisitos

1. Conta no GitHub
2. Conta no Streamlit Community Cloud (https://streamlit.io/cloud)

## 🔧 Preparação

### 1. Criar Repositório no GitHub

```bash
# Inicializar Git (se não estiver inicializado)
git init

# Adicionar arquivos
git add .
git commit -m "Initial commit"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### 2. Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Clique em **"New app"**
3. Conecte sua conta do GitHub
4. Selecione:
   - Repository: `SEU_USUARIO/SEU_REPOSITORIO`
   - Branch: `main`
   - Main file path: `main.py`
5. Clique em **"Deploy!"**

### 3. Configurar Secrets (Variáveis de Ambiente)

No painel do Streamlit Cloud:

1. Vá em **Settings > Secrets**
2. Adicione suas variáveis:

```toml
# Email para notificações
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_app"
EMAIL_RECEIVER = "destinatario@gmail.com"
```

## 📦 Arquivos Necessários

✅ `requirements.txt` - Dependências Python  
✅ `main.py` - Arquivo principal do Streamlit  
✅ `.streamlit/config.toml` - Configurações (opcional)  
✅ `database.py` - Módulo de banco de dados  
✅ `config.py` - Configurações da aplicação

## 🔗 Estrutura para Deploy

```
Robo_Investimentos/
├── main.py                    # Arquivo principal
├── config.py                  # Configurações
├── database.py                # Banco de dados
├── requirements.txt           # Dependências
├── .streamlit/
│   └── config.toml           # Configurações Streamlit
└── data/                      # Será criado automaticamente
    └── investimentos.db
```

## ⚙️ Requisitos Importantes

- O Streamlit Community Cloud tem **1GB de RAM**
- Limite de **1GB de armazenamento**
- ✅ **BACKUP AUTOMÁTICO CONFIGURADO**: Os dados agora persistem via Google Sheets!
- 📖 Veja [CONFIGURAR_BACKUP_PERSISTENTE.md](CONFIGURAR_BACKUP_PERSISTENTE.md) para instruções

## 🌐 Após Deploy

Sua aplicação estará disponível em:
```
https://SEU_APP.streamlit.app
```

## 🔄 Atualizações

Qualquer push para o branch `main` no GitHub fará deploy automático!

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
