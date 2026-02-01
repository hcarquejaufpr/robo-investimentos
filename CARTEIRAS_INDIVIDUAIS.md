# 👥 Sistema de Carteiras Individualizadas

## 🎯 Como Funciona

Cada usuário tem sua **própria carteira privada** e independente!

## ✨ Recursos

### 1. **Carteiras Separadas**
- ✅ Cada usuário vê apenas seus próprios ativos
- ✅ Configurações independentes (multiplicadores ATR)
- ✅ Histórico próprio de edições

### 2. **Gestão Individual**
- Adicione suas ações americanas
- Configure seus FIIs brasileiros
- Registre seus títulos do Tesouro Direto
- Ajuste os multiplicadores do seu perfil

### 3. **Privacidade Total**
- Usuário A não vê carteira do Usuário B
- Cada um edita apenas sua própria carteira
- Dados salvos localmente ou no Streamlit Cloud

## 📊 Exemplo de Uso

### Família:
- **João** (admin): Ações tech (NVDA, AAPL, GOOGL)
- **Maria** (maria): FIIs e dividendos (HGLG11, MXRF11)
- **Pedro** (pedro): Portfolio misto

### Sócios:
- **Sócio A**: Carteira conservadora
- **Sócio B**: Carteira agressiva

## 💾 Armazenamento

### Local (PC):
```
user_portfolios.json
{
  "admin": {
    "US_STOCKS": ["AAPL", "NVDA"],
    "BR_FIIS": ["HGLG11.SA"],
    ...
  },
  "maria": {
    "US_STOCKS": [],
    "BR_FIIS": ["MXRF11.SA", "VISC11.SA"],
    ...
  }
}
```

### Streamlit Cloud:
Configure em **Settings > Secrets** (opcional)

## 🔐 Segurança

- ✅ Arquivo `user_portfolios.json` **NÃO** sobe para o Git
- ✅ Cada usuário acessa apenas após login
- ✅ Dados isolados por usuário

## 🚀 Como Usar

1. **Faça login** com seu usuário
2. **Configure sua carteira** na barra lateral
3. **Salve** - Suas configurações ficam privadas
4. **Outros usuários** não veem seus ativos!

## 📝 Fluxo Completo

```
1. Login (admin)
   ↓
2. Vê carteira do admin
   ↓
3. Edita e salva
   ↓
4. Logout
   ↓
5. Login (maria)
   ↓
6. Vê carteira da maria (diferente!)
```

Cada usuário tem sua própria experiência! 🎉
