"""
Arquivo de Configuração do Robô de Investimentos
================================================
Altere os tickers e datas conforme sua carteira real.
"""

# ============================================================================
# AÇÕES AMERICANAS
# ============================================================================
US_STOCKS = ['AAPL', 'AMZN', 'GOOGL', 'NVDA', 'TSLA', 'XOM']

# ============================================================================
# FUNDOS IMOBILIÁRIOS BRASILEIROS (FIIs)
# ============================================================================
BR_FIIS = ['HGLG11.SA', 'KNIP11.SA', 'VISC11.SA', 'MXRF11.SA']

# ============================================================================
# TESOURO DIRETO
# ============================================================================
TESOURO_DIRETO = {'Tesouro Selic 2027': {'data_compra': '2024-02-15'}, 'Tesouro IPCA+ 2035': {'data_compra': '2023-01-10'}, 'Tesouro Prefixado 2029': {'data_compra': '2024-08-20'}}

# ============================================================================
# PARÂMETROS DE ANÁLISE TÉCNICA
# ============================================================================
PARAMETROS = {
    'MULTIPLIER_US': 1.2,   # Ações americanas (mais conservador para saída estratégica)
    'MULTIPLIER_BR': 1.0,   # FIIs brasileiros (mais conservador)
}
