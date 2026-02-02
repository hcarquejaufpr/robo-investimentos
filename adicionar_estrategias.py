"""
Script para adicionar estratégias aos títulos já cadastrados
"""

import database as db
import sys
sys.path.insert(0, 'c:\\RAG\\Robo_Investimentos')
from main import adicionar_estrategias_tesouro

USERNAME = "admin"

def adicionar_estrategias():
    """Adiciona estratégias aos títulos do Tesouro"""
    # Carrega portfolio
    portfolio = db.load_user_portfolio(USERNAME)
    
    if not portfolio or "TESOURO_DIRETO" not in portfolio:
        print("❌ Nenhum título encontrado!")
        return
    
    tesouro = portfolio["TESOURO_DIRETO"]
    
    print(f"📊 Títulos encontrados: {len(tesouro)}")
    print("\nTítulos SEM estratégia:")
    for nome, dados in tesouro.items():
        if 'estrategia' not in dados:
            print(f"  ❌ {nome}")
    
    # Adiciona estratégias
    print("\n🔄 Adicionando estratégias...")
    tesouro_com_estrategia = adicionar_estrategias_tesouro(tesouro)
    
    # Atualiza no banco
    portfolio["TESOURO_DIRETO"] = tesouro_com_estrategia
    db.save_user_portfolio(USERNAME, portfolio)
    
    print("\n✅ Estratégias adicionadas com sucesso!")
    print("\nTítulos COM estratégia:")
    for nome, dados in tesouro_com_estrategia.items():
        if 'estrategia' in dados:
            print(f"  ✅ {nome}: {dados['estrategia']} (Semana {dados.get('semana_venda', 1)})")

if __name__ == "__main__":
    adicionar_estrategias()
