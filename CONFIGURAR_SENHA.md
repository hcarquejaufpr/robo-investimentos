# 🔒 Sistema de Múltiplos Usuários

## ✨ Funcionalidades
- ✅ **Cadastro** de novos usuários
- ✅ **Login** individual
- ✅ **Logout** seguro
- ✅ Cada usuário pode ter configurações próprias

## 🚀 Como Usar

### 1. **Primeiro Acesso (Usuário Padrão)**
   - **Usuário:** `admin`
   - **Senha:** `investidor2026`

### 2. **Criar Nova Conta**
   - Clique na aba **"📝 Cadastro"**
   - Preencha:
     - Nome de usuário
     - Seu nome completo
     - Senha (mínimo 6 caracteres)
     - Confirme a senha
   - Clique em **"Cadastrar"**

### 3. **Fazer Login**
   - Use seu usuário e senha
   - Acesse seu dashboard personalizado

### 4. **Sair**
   - Clique no botão **"🚪 Sair"** no canto superior direito

## 🛡️ Segurança

### Local (PC)
- Usuários salvos em `users.json` (não commitado no Git)
- Senha padrão: `investidor2026`

### Streamlit Cloud (Recomendado)
Configure usuários permanentes em **Settings > Secrets**:

```toml
users = '''
{
  "admin": {
    "password": "sua_senha_forte",
    "name": "Administrador"
  },
  "usuario2": {
    "password": "outra_senha",
    "name": "João Silva"
  }
}
'''
```

## 📝 Próximas Melhorias (Futuro)
- [ ] Carteira individualizada por usuário
- [ ] Recuperação de senha por email
- [ ] Níveis de permissão (admin, usuário)
- [ ] Criptografia de senhas (bcrypt)
