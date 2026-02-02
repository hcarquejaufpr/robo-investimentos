# 🤖 Robô de Investimentos - Estratégia de Saída

Sistema inteligente para monitoramento de carteira de investimentos (Brasil e EUA) com análise técnica e otimização fiscal.

## 📊 Funcionalidades

### 🎯 Preços de Stop (NOVO!)
- **Valores Calculados Automaticamente**: Disparo e Limite para Stop Loss e Stop Gain
- **Para Uso no Home Broker**: Copie e cole direto na sua corretora
- **Baseado em ATR**: Ajustado automaticamente pela volatilidade
- **Simples e Prático**: 4 colunas extras na tabela

📖 **Ver:** [GUIA_STOP_SIMPLES.md](GUIA_STOP_SIMPLES.md) para tutorial completo

### Renda Variável
- **ATR (Average True Range)**: Mede volatilidade
- **Trailing Stop Loss**: Preço de saída automatizado
- **Análise de Tendência**: SMA 20 períodos
- Suporte para ações americanas e FIIs brasileiros

### Tesouro Direto
- **Otimização Fiscal**: Calcula a melhor data de venda
- **Tabela Regressiva de IR**: 22.5% → 15%
- **Alertas Inteligentes**: Avisa quando esperar reduz imposto

## 🚀 Como Usar

1. Configure seus ativos no painel lateral
2. Ajuste os multiplicadores de stop conforme seu perfil
3. Clique em "Salvar Configurações"
4. Analise as recomendações de saída

## 🛠️ Tecnologias

- Python 3.12
- Streamlit (Interface Web)
- yfinance (Dados de mercado)
- pandas (Análise de dados)

## 📝 Configuração

Edite `config.py` ou use a interface web para adicionar:
- Ações americanas (ex: AAPL, NVDA)
- FIIs brasileiros (ex: HGLG11.SA)
- Títulos do Tesouro com datas de compra

## 🗄️ Persistência de Dados

O sistema utiliza **SQLite** com volumes Docker para garantir que seus dados não sejam perdidos:
- ✅ Usuários e senhas persistem entre reinicializações
- ✅ Carteiras individuais salvas automaticamente
- ✅ Histórico completo de operações
- ✅ Migração automática de arquivos JSON antigos

📖 **Ver:** [DATABASE_GUIDE.md](DATABASE_GUIDE.md) para mais detalhes

## 📚 Documentação Adicional

- 🎯 [GUIA_STOP_SIMPLES.md](GUIA_STOP_SIMPLES.md) - **Como usar os preços de Stop**
- 📁 [CARTEIRAS_INDIVIDUAIS.md](CARTEIRAS_INDIVIDUAIS.md) - Sistema multi-usuário
- 🔑 [CONFIGURAR_SENHA.md](CONFIGURAR_SENHA.md) - Autenticação e segurança
- 📧 [CONFIGURAR_EMAIL.md](CONFIGURAR_EMAIL.md) - Notificações por email
- 🐳 [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Deploy com Docker
- 🗄️ [DATABASE_GUIDE.md](DATABASE_GUIDE.md) - Banco de dados persistente

## ⚠️ Aviso Legal

Este sistema é apenas para fins educacionais. Não constitui recomendação de investimento. Consulte um profissional certificado antes de tomar decisões financeiras.
