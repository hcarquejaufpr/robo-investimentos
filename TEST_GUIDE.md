# 🧪 Guia de Testes

## 📋 Testes Disponíveis

### 1. Teste do SQLite Database

Verifica se o banco de dados está funcionando corretamente.

```powershell
python test_sqlite.py
```

**O que testa:**
- ✅ Criação do banco de dados
- ✅ Criação de usuários
- ✅ Salvamento de carteiras
- ✅ Carregamento de dados
- ✅ Persistência de dados

**Resultado esperado:**
```
✅ TODOS OS TESTES PASSARAM!
```

---

### 2. Teste de Notificações por Email

Verifica se o sistema de email está configurado corretamente.

**Antes de executar:**

1. Configure as variáveis de ambiente:
```powershell
$env:EMAIL_PASSWORD="sua_senha_app_gmail"
$env:EMAIL_RECEIVER="seuemail@gmail.com"
```

2. Ou edite o arquivo `test_email.py` linha 17:
```python
RECEIVER_EMAIL = "seuemail@gmail.com"  # ← ALTERE AQUI
```

3. Execute:
```powershell
python test_email.py
```

**O que testa:**
- ✅ Conexão com servidor SMTP do Gmail
- ✅ Autenticação com senha de app
- ✅ Envio de email HTML
- ✅ Formatação do relatório

**Resultado esperado:**
```
✅ EMAIL ENVIADO COM SUCESSO!
📬 Verifique a caixa de entrada: seuemail@gmail.com
```

---

### 3. Teste Docker (Local)

Verifica se a aplicação roda corretamente no Docker.

```powershell
docker-compose up --build
```

**O que testa:**
- ✅ Build da imagem Docker
- ✅ Instalação de dependências
- ✅ Inicialização do Streamlit
- ✅ Montagem de volumes

**Acesso:**
```
http://localhost:8501
```

**Para parar:**
```powershell
docker-compose down
```

---

### 4. Teste Completo

Executa todos os testes automaticamente:

```powershell
python test_all.py
```

---

## 🔧 Solução de Problemas

### Erro no SQLite

**Problema:** "Permission denied" ou "Database locked"

**Solução:**
```powershell
# Remove banco antigo e recria
Remove-Item data/robo_investimentos.db -Force
python test_sqlite.py
```

---

### Erro no Email

**Problema:** "SMTPAuthenticationError"

**Soluções:**

1. **Gere uma Senha de App do Google:**
   - Acesse: https://myaccount.google.com/apppasswords
   - Crie senha para "E-mail"
   - Use essa senha de 16 caracteres

2. **Configure a variável de ambiente:**
   ```powershell
   $env:EMAIL_PASSWORD="xxxx xxxx xxxx xxxx"
   ```

3. **Ou configure no Streamlit Cloud:**
   - Settings > Secrets
   ```toml
   EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx"
   EMAIL_SENDER = "seuemail@gmail.com"
   ```

---

### Erro no Docker

**Problema:** "docker: command not found"

**Solução:**
1. Verifique se o Docker Desktop está rodando
2. Execute como Administrador:
   ```powershell
   docker --version
   ```

**Problema:** "Port 8501 already in use"

**Solução:**
```powershell
# Para o processo usando a porta
Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process -Force

# Ou mude a porta no docker-compose.yml:
# ports:
#   - "8502:8501"
```

---

## 📊 Verificação no Streamlit Cloud

Para verificar se tudo está funcionando em produção:

1. **Acesse o dashboard:**
   https://share.streamlit.io/

2. **Clique no seu app**

3. **Verifique:**
   - ✅ Status: "Running"
   - ✅ Logs sem erros
   - ✅ Últmo deploy bem-sucedido

4. **Teste a aplicação:**
   - Faça login
   - Cadastre um ativo
   - Configure notificações
   - Envie email de teste

---

## 🎯 Checklist de Validação

Use este checklist para garantir que tudo está funcionando:

### Banco de Dados
- [ ] Usuários são criados e salvos
- [ ] Login funciona
- [ ] Carteiras são persistidas
- [ ] Dados sobrevivem ao reiniciar

### Sistema de Email
- [ ] Email de teste é recebido
- [ ] Formatação HTML está correta
- [ ] Email do usuário é usado automaticamente
- [ ] Notificações diárias funcionam

### Docker
- [ ] Container inicia sem erros
- [ ] App acessível em localhost:8501
- [ ] Volumes montados corretamente
- [ ] Hot reload funciona

### Streamlit Cloud
- [ ] Deploy bem-sucedido
- [ ] App acessível publicamente
- [ ] Login funciona
- [ ] Dados persistem entre sessões
- [ ] Notificações enviadas corretamente

---

## 💡 Dicas

- Execute os testes sempre que fizer mudanças importantes
- Configure os secrets antes de testar emails
- Use o Docker para testar em ambiente similar à produção
- Verifique os logs do Streamlit Cloud para debug

---

## 🆘 Precisa de Ajuda?

Se algo não funcionar:

1. Verifique os logs
2. Execute os testes individuais
3. Consulte a documentação específica:
   - [DATABASE_GUIDE.md](DATABASE_GUIDE.md)
   - [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
   - [DEPLOY_STREAMLIT.md](DEPLOY_STREAMLIT.md)
