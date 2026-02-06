"""
Adiciona quantidade de cotas do FII HGRE11.SA para o usuário hcarqueja
"""
import database as db

print("="*80)
print("ADICIONANDO QUANTIDADE DO FII HGRE11.SA")
print("="*80)

username = 'hcarqueja'

# Carrega carteira atual
portfolio = db.load_user_portfolio(username)

if portfolio is None:
    print(f"\n❌ Usuário {username} não tem carteira cadastrada!")
else:
    print(f"\n✅ Carteira encontrada!")
    print(f"   FIIs cadastrados: {portfolio['BR_FIIS']}")
    
    # Solicita quantidade
    print(f"\n💡 Digite a quantidade de cotas do HGRE11.SA:")
    try:
        quantidade = float(input("Quantidade: ").strip())
        
        # Atualiza quantidade
        if 'ASSET_QUANTITIES' not in portfolio:
            portfolio['ASSET_QUANTITIES'] = {}
        
        portfolio['ASSET_QUANTITIES']['HGRE11.SA'] = quantidade
        
        # Salva no banco
        print(f"\n💾 Salvando no banco de dados...")
        success = db.save_user_portfolio(username, portfolio)
        
        if success:
            print(f"\n✅ Quantidade salva com sucesso!")
            print(f"   HGRE11.SA: {quantidade} cotas")
            print(f"\n🌐 Backup automático executado no Google Sheets!")
            print(f"   🔗 Acesse: https://docs.google.com/spreadsheets/d/1m_D8SB1g-r2g6w96lzh5U9asrQfE4lFMwW3RXzDz9eE")
            print(f"   📄 Aba: Carteira_{username}")
        else:
            print(f"\n❌ Erro ao salvar!")
    
    except ValueError:
        print(f"\n❌ Valor inválido!")
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Operação cancelada pelo usuário")

print("\n" + "="*80)
