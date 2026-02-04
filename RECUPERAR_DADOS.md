# 🔄 Recuperar Dados Perdidos no Streamlit Cloud

## ⚠️ Problema

O Streamlit Cloud **não mantém dados do SQLite** quando o app é reiniciado. Isso significa que:
- Usuários cadastrados são perdidos
- Carteiras cadastradas são perdidas
- É necessário fazer backup e restore manual

## ✅ Solução Implementada

O sistema agora possui **backup automático** dos usuários:

### 1. Backup Automático
- Sempre que um novo usuário é cadastrado, um backup é criado em `data/users_backup.json`
- Este arquivo deve ser **commitado no Git** para persistir no Streamlit Cloud

### 2. Restore Automático
- Quando o banco estiver vazio, o sistema automaticamente restaura os usuários do backup
- Isso acontece na inicialização do app

## 🛠️ Como Recuperar Seu Usuário (hcarqueja)

### Opção 1: Criar Localmente e Fazer Deploy

1. **Execute o script de recuperação localmente:**
```bash
python criar_usuario_hcarqueja.py
```

2. **Siga as instruções** para informar:
   - Senha
   - Nome completo
   - Email

3. **Verifique o backup criado:**
```bash
# O arquivo data/users_backup.json foi criado
cat data/users_backup.json
```

4. **Commit e push para o GitHub:**
```bash
git add data/users_backup.json
git commit -m "Adiciona backup de usuários"
git push
```

5. **Aguarde o deploy automático** no Streamlit Cloud
   - O app será reiniciado automaticamente
   - Os usuários serão restaurados do backup

### Opção 2: Cadastrar Novamente no Streamlit Cloud

1. Acesse: https://robo-investimentos.streamlit.app
2. Vá para a aba **"Cadastro"**
3. Cadastre-se novamente com:
   - Usuário: `hcarqueja`
   - Senha: (sua senha original)
   - Nome e email

**⚠️ IMPORTANTE:** Use exatamente o mesmo usuário para poder recuperar a carteira posteriormente

## 📊 Recuperar Carteira

Se você tinha uma carteira cadastrada, ela pode estar em:

1. **Backup manual** (se você fez antes)
2. **Logs do Streamlit** (pergunte ao suporte)
3. **Arquivo de importação** (se você exportou anteriormente)

### Para Exportar Carteira Atual (proteção futura):

No menu lateral do app, use a opção:
- **"💾 Backup de Dados"** → Download dos dados em JSON
- Guarde este arquivo em local seguro

## 🔐 Dados do Seu Usuário

Para referência futura, anote suas credenciais:

```
Usuário: hcarqueja
Senha: [sua senha]
Nome: [seu nome]
Email: [seu email]
```

## 🚀 Melhorias Futuras

Para evitar perda de dados no futuro, considere:

1. **Usar banco de dados externo** (PostgreSQL, MongoDB Atlas)
2. **Sistema de backup automático para cloud storage** (Google Drive, Dropbox)
3. **Deploy em servidor próprio** com Docker

## 📞 Suporte

Se precisar de ajuda para recuperar dados:
- Email: admin@robo-investimentos.com
- Informe seu usuário (hcarqueja) e a data aproximada do último acesso
