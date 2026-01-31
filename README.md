# 🤖 Robô de Investimentos - Estratégia de Saída

Sistema inteligente para monitoramento de carteira de investimentos (Brasil e EUA) com análise técnica e otimização fiscal.

## 📊 Funcionalidades

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

## ⚠️ Aviso Legal

Este sistema é apenas para fins educacionais. Não constitui recomendação de investimento. Consulte um profissional certificado antes de tomar decisões financeiras.
