# 🧪 Como Testar o Banco de Dados Online (Streamlit Cloud)

## 1️⃣ Acesse o Painel de Gerenciamento

1. Vá para: https://share.streamlit.io/
2. Faça login com sua conta do GitHub
3. Encontre o app **robo-investimentos**
4. Clique no nome do app

## 2️⃣ Verifique os Logs do Deploy

Na página do app, você verá:
- **Status**: "Running" (verde) = funcionando
- **Logs**: Clique em "Logs" para ver mensagens do servidor

### O que procurar nos logs:

```
✅ Banco de dados inicializado: /mount/src/.../data/robo_investimentos.db
📊 Usuários no banco: [{'username': 'admin', 'email': '...'}]
```

Se essas mensagens aparecem, o banco está funcionando!

## 3️⃣ Teste de Login

1. Acesse seu app: https://robo-investimentos-hcarqueja.streamlit.app
2. Tente fazer login com:
   - **Usuário:** admin
   - **Senha:** investidor2026
3. Se entrar, o banco está salvando usuários ✅

## 4️⃣ Teste de Persistência de Dados

### Teste com Quantidades:

1. Faça login no app online
2. Adicione uma quantidade (ex: AAPL = 1.5)
3. Clique em "💾 SALVAR QUANTIDADES AGORA"
4. Clique em "🔄 Atualizar Cotações"
5. **Feche o navegador completamente**
6. Abra novamente e faça login
7. Verifique se a quantidade continua salva

Se a quantidade aparecer novamente, o banco está persistindo! ✅

### Teste com Novo Usuário:

1. Vá na aba "Cadastro"
2. Crie um usuário: `teste_cloud`
3. Senha: `teste123`
4. Email: `teste@email.com`
5. **Feche o navegador**
6. Abra novamente
7. Tente fazer login com `teste_cloud`

Se conseguir logar, o banco está salvando usuários! ✅

## 5️⃣ Verificar Arquivos Salvos

No Streamlit Cloud:
1. Vá em "Settings" → "Advanced settings"
2. Procure por "Secrets" (para variáveis de ambiente)
3. O banco SQLite fica em: `/mount/src/robo-investimentos/data/`

⚠️ **Importante:** O Streamlit Cloud pode resetar o banco se o app ficar inativo por muito tempo ou se houver um redeploy. Para persistência real, considere usar:
- PostgreSQL (Supabase)
- Google Cloud SQL
- Amazon RDS

## 6️⃣ Comparar Local vs Cloud

Execute este teste em ambos:

### Local:
```powershell
python -c "import database as db; db.init_database(); users = db.load_users(); print('Users:', list(users.keys()))"
```

### Cloud:
Adicione temporariamente no `main.py` (após `db.init_database()`):
```python
st.sidebar.write(f"🔍 Usuários no banco: {list(db.load_users().keys())}")
```

Faça commit e aguarde o deploy. Se a lista aparecer na sidebar, o banco está funcionando!

## 🚨 Problemas Comuns

### "Usuário não encontrado" após criar conta
- O banco pode ter sido resetado pelo Streamlit Cloud
- Solução: Use PostgreSQL ou outro DB externo

### Quantidades desaparecem
- Streamlit Cloud pode limpar arquivos temporários
- Solução: Migrar para banco externo persistente

### Login funcionando local mas não na cloud
- Verifique os logs de erro no painel do Streamlit
- Pode ser problema de permissões de arquivo

## ✅ Banco Funcionando = 

- Login funciona após reload
- Quantidades persistem após fechar navegador
- Múltiplos usuários podem ser criados e recuperados
- Logs mostram "Banco de dados inicializado"

---

**Dica:** Para produção, recomendo migrar para **Supabase** (PostgreSQL gratuito) que garante persistência real dos dados!
