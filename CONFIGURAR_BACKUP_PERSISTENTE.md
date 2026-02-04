# 💾 Configurar Backup Persistente no Streamlit Cloud

## 🎯 Objetivo

Fazer o banco de dados SQLite persistir entre reinicializações do Streamlit Cloud usando **Google Sheets** como armazenamento remoto.

---

## 📋 Como Funciona

1. **Backup Automático**: Sempre que houver alterações no banco (novo usuário, carteira atualizada), os dados são automaticamente salvos no Google Sheets
2. **Restore Automático**: Quando o app iniciar, verifica se o banco está vazio e restaura automaticamente do Google Sheets
3. **Fallback Local**: Se Google Sheets não estiver configurado, usa backup JSON local (não persiste no Streamlit Cloud)

---

## 🔧 Passo a Passo - Configuração Google Sheets

### 1️⃣ Criar Service Account no Google Cloud

1. Acesse: [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. No menu lateral (☰), navegue até **"IAM e administrador"** → **"Contas de serviço"**
   - Ou use a busca: digite `contas de serviço`
4. Clique em **"+ CRIAR CONTA DE SERVIÇO"** (botão azul no topo)
5. Preencha:
   - **Nome da conta de serviço**: `robo-investimentos-backup`
   - **ID da conta de serviço**: será preenchido automaticamente
   - **Descrição**: `Backup automático do Robo Investimentos`
6. Clique em **"CRIAR E CONTINUAR"**
7. Em "Conceder acesso ao projeto": **Pule** (clique em **"CONTINUAR"** sem selecionar função)
8. Em "Conceder acesso de usuários": **Pule** também (clique em **"CONCLUÍDO"**)

### 2️⃣ Criar Chave JSON

1. Na lista de Contas de serviço, clique no **email** da conta que você criou
2. Vá para a aba **"CHAVES"** (no topo da página)
3. Clique em **"ADICIONAR CHAVE"** → **"Criar nova chave"**
4. Escolha tipo **JSON** 
5. Clique em **"CRIAR"**
6. Um arquivo JSON será baixado automaticamente → **Guarde muito bem esse arquivo!**

### 3️⃣ Habilitar APIs Necessárias
**Opção 1 - Links diretos (mais rápido):**
- **API Google Sheets**: https://console.cloud.google.com/apis/library/sheets.googleapis.com
  - Clique em **"ATIVAR"**
- **API Google Drive**: https://console.cloud.google.com/apis/library/drive.googleapis.com
  - Clique em **"ATIVAR"**

**Opção 2 - Pela interface:**
1. No menu ☰ → **"APIs e serviços"** → **"Biblioteca"**
2. Plique no **+** (Criar nova planilha em branco)
3. Renomeie a planilha para: **`RoboInvestimentos_Backup`** (clique no nome "Planilha sem título" no topo)
4. Clique no botão **"Compartilhar"** (canto superior direito)
5. **Adicione o email da conta de serviço**:
   - Abra o arquivo JSON que você baixou (com bloco de notas)
   - Procure a linha `"client_email":` e copie o email (algo como: `robo-investimentos-backup@seu-projeto.iam.gserviceaccount.com`)
   - Cole esse email no campo "Adicionar pessoas e grupos"
   - Certifique-se que está como **"Editor"** (não apenas Leitor)
   - Clique em **"Enviar"** (pode desmarcar "Notificar pessoas")

1. Acesse [Google Sheets](https://sheets.google.com)
2. Crie uma nova planilha chamada: **`RoboInvestimentos_Backup`**
3. Compartilhe a planilha com o **email do Service Account**:
   - Abra o arquivo JSON baixado
   - Copie o email em `"client_email"` (algo como: `robo-investimentos-backup@...gserviceaccount.com`)
   - No Google Sheets: **Compartilhar > Adicionar email > Editor**
Clique no seu app na lista
3. Clique no menu **"⋮"** (três pontinhos) → **"Settings"** (Configurações)
4. No menu lateral, clique em **"Secrets"**
5. Cole o seguinte, substituindo com os dados do seu arquivo JSON

1. Acesse seu app no [Streamlit Cloud](https://share.streamlit.io/)
2. Vá em **"Settings" > "Secrets"**
3. Adicione o conteúdo completo do arquivo JSON baixado:

```toml
[gcp_service_account]
type = "service_account"
project_id = "seu-projeto-id"
private_key_id = "sua-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_PRIVADA_AQUI\n-----END PRIVATE KEY-----\n"
client_email = "robo-investimentos-backup@seu-projeto.iam.gserviceaccount.com"
client_id = "seu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/seu-email"

# Nome da planilha (opcional, padrão: RoboInvestimentos_Backup)
backup_sheet_name = "RoboInvestimentos_Backup"
```

⚠️ **IMPORTANTE**: 
- Copie TODO o conteúdo do arquivo JSON
- A `private_key` deve manter os `\n` para quebras de linha
- Não compartilhe essas credenciais publicamente

### 6️⃣ Deploy e Teste

1. Faça commit e push das alterações:
```bash
git add .
git commit -m "Adicionar backup persistente com Google Sheets"
git push
```

2. O Streamlit Cloud fará deploy automático
3. Teste criando um usuário e reiniciando o app (botão "Reboot app")
4. O usuário deve ser restaurado automaticamente!

---

## ✅ Verificação

Para confirmar que está funcionando:

1. **No Console Python** (logs do Streamlit Cloud):
   ```
   ✅ Backup realizado no Google Sheets: 2026-02-04 15:30:45
   ```

2. **Na Planilha Google Sheets**:
   - Abra a planilha `RoboInvestimentos_Backup`
   - Verá uma worksheet chamada `backup`
   - Célula A1 terá o JSON com todos os dados

---

## 🔍 Troubleshooting

### ❌ "Credenciais Google Sheets não configuradas"
- Verifique se copiou TODO o conteúdo do JSON no Streamlit Secrets
- Confirme que a seção começa com `[gcp_service_account]`

### ❌ "Planilha de backup não encontrada"
- Confirme que criou a planilha com nome exato: `RoboInvestimentos_Backup`
- Compartilhe com o email do service account como **Editor**

### ❌ "Permission denied"
- Certifique-se que habilitou Google Sheets API e Google Drive API
- Verifique se o service account tem permissão de Editor na planilha

### ❌ Backup não está sendo salvo
- Verifique os logs do Streamlit Cloud para erros
- Teste localmente primeiro com `streamlit run main.py`

---

## 🧪 Testar Localmente

Para testar antes de fazer deploy:

1. Crie arquivo `.streamlit/secrets.toml` localmente:
```toml
[gcp_service_account]
type = "service_account"
# ... resto das credenciais
```

2. Execute: `streamlit run main.py`
3. Crie um usuário e veja se aparece no Google Sheets

⚠️ **NUNCA FAÇA COMMIT** do arquivo `secrets.toml`! Adicione ao `.gitignore`:
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

---

## 📊 Estrutura do Backup

O backup salva:
- ✅ Todos os usuários (username, senha, nome, email)
- ✅ Todas as carteiras (ações, FIIs, Tesouro Direto)
- ✅ Quantidades de ativos
- ✅ Parâmetros e multiplicadores
- ✅ Histórico de operações
- ✅ Snapshots de portfólio
- ✅ Data/hora do backup

---

## 🎉 Pronto!

Agora seu banco de dados **persiste** mesmo quando o Streamlit Cloud desativa ou reinicia o app! 🚀

Os dados são:
- 💾 Salvos automaticamente a cada alteração
- 🔄 Restaurados automaticamente ao iniciar
- 🌐 Acessíveis via Google Sheets (pode ver e exportar)
- 🔒 Seguros com autenticação Google

---

## 🔗 Links Úteis

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [Streamlit Secrets Docs](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [gspread Documentation](https://docs.gspread.org/)
