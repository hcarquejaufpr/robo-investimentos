# 🔒 Como Configurar a Senha no Streamlit Cloud

## Passo 1: Acesse seu app no Streamlit Cloud
- Vá em: https://share.streamlit.io
- Clique em "My apps"
- Selecione seu app `robo-investimentos`

## Passo 2: Configure a senha personalizada
1. Clique no menu **⋮** (3 pontinhos) do app
2. Selecione **"Settings"**
3. Vá na aba **"Secrets"**
4. Cole o seguinte código:

```toml
password = "SUA_SENHA_AQUI"
```

5. **Substitua** `SUA_SENHA_AQUI` pela sua senha desejada
6. Clique em **"Save"**

## Passo 3: Teste
- Recarregue seu app
- Digite a nova senha para acessar

## 🛡️ Segurança
- ✅ A senha NÃO fica no código público do GitHub
- ✅ Só você tem acesso às configurações de Secrets
- ✅ A senha é criptografada no Streamlit Cloud

## 📝 Senha Padrão Local
Quando rodando localmente: `investidor2026`
