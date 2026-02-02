"""
Script para cadastrar títulos do Tesouro Direto do usuário
Execute este script para cadastrar automaticamente
"""

import database as db

# Dados extraídos do Excel do usuário
TITULOS_USUARIO = {
    "Tesouro IPCA+ 2045": {
        "data_compra": "2024-01-01",  # Data genérica
        "valor_investido": 214.55
    },
    "Tesouro IPCA+ com Juros Semestrais 2035": {
        "data_compra": "2024-01-01",
        "valor_investido": 1528.00
    },
    "Tesouro IPCA+ com Juros Semestrais 2040": {
        "data_compra": "2024-01-01",
        "valor_investido": 9663.15
    },
    "Tesouro IPCA+ com Juros Semestrais 2055": {
        "data_compra": "2024-01-01",
        "valor_investido": 15006.94
    },
    "Tesouro Prefixado 2026": {
        "data_compra": "2024-01-01",
        "valor_investido": 1798.10
    },
    "Tesouro Prefixado 2028": {
        "data_compra": "2024-01-01",
        "valor_investido": 11960.93
    },
    "Tesouro Prefixado 2029": {
        "data_compra": "2024-01-01",
        "valor_investido": 1340.73
    },
    "Tesouro Prefixado com Juros Semestrais 2033": {
        "data_compra": "2024-01-01",
        "valor_investido": 18973.14
    },
    "Tesouro Selic 2026": {
        "data_compra": "2024-01-01",
        "valor_investido": 4701.20
    },
    "Tesouro Selic 2027": {
        "data_compra": "2024-01-01",
        "valor_investido": 44625.86
    },
    "Tesouro Selic 2029": {
        "data_compra": "2024-01-01",
        "valor_investido": 672.46
    }
}

# Username do usuário
USERNAME = "admin"  # Ajuste se necessário

def cadastrar_titulos():
    """Cadastra os títulos no banco de dados"""
    # Carrega portfolio atual
    portfolio = db.load_user_portfolio(USERNAME)
    
    if portfolio is None:
        portfolio = {
            "US_STOCKS": [],
            "BR_FIIS": [],
            "TESOURO_DIRETO": {},
            "ASSET_QUANTITIES": {},
            "PARAMETROS": {"MULTIPLIER_US": 1.2, "MULTIPLIER_BR": 1.0},
            "INDIVIDUAL_MULTIPLIERS": {},
            "OPERATIONS_HISTORY": [],
            "PORTFOLIO_SNAPSHOTS": []
        }
    
    # Adiciona títulos
    portfolio["TESOURO_DIRETO"] = TITULOS_USUARIO
    
    # Salva no banco
    db.save_user_portfolio(USERNAME, portfolio)
    
    total_investido = sum(t["valor_investido"] for t in TITULOS_USUARIO.values())
    
    print("✅ Títulos cadastrados com sucesso!")
    print(f"📊 Total de títulos: {len(TITULOS_USUARIO)}")
    print(f"💰 Total investido: R$ {total_investido:,.2f}")
    print("\nTítulos cadastrados:")
    for nome, dados in TITULOS_USUARIO.items():
        print(f"  • {nome}: R$ {dados['valor_investido']:,.2f}")

if __name__ == "__main__":
    cadastrar_titulos()
