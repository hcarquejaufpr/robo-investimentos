"""
Diagnóstico Completo - Verificar por que a quantidade não aparece
"""
import database as db
import json

print("="*80)
print("🔍 DIAGNÓSTICO COMPLETO - QUANTIDADE NÃO APARECE NA INTERFACE")
print("="*80)

username = 'hcarqueja'

print(f"\n1️⃣ VERIFICANDO BANCO DE DADOS SQLite:")
print("-" * 80)

portfolio = db.load_user_portfolio(username)

if portfolio:
    print(f"✅ Carteira encontrada no banco")
    
    print(f"\n📊 BR_FIIS: {portfolio.get('BR_FIIS', [])}")
    
    print(f"\n🔢 ASSET_QUANTITIES:")
    quantities = portfolio.get('ASSET_QUANTITIES', {})
    print(f"   Tipo: {type(quantities)}")
    print(f"   Conteúdo: {quantities}")
    
    if quantities:
        for ticker, qty in quantities.items():
            print(f"\n   Ticker: {ticker}")
            print(f"   Tipo do valor: {type(qty)}")
            print(f"   Valor: {qty}")
            if isinstance(qty, dict):
                print(f"   Quantidade: {qty.get('quantidade', 'N/A')}")
    else:
        print("   ⚠️ ASSET_QUANTITIES está vazio!")
    
    print(f"\n📋 Estrutura completa do portfolio:")
    print(f"   Keys: {list(portfolio.keys())}")
else:
    print("❌ Carteira NÃO encontrada")

print("\n" + "="*80)
print("2️⃣ VERIFICANDO DIRETAMENTE NO BANCO SQLite (raw):")
print("-" * 80)

import sqlite3
conn = sqlite3.connect('data/robo_investimentos.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('''
    SELECT id, username, asset_quantities, updated_at 
    FROM portfolios 
    WHERE username = ? 
    ORDER BY id DESC 
    LIMIT 1
''', (username,))

row = cursor.fetchone()

if row:
    print(f"✅ Registro encontrado:")
    print(f"   ID: {row['id']}")
    print(f"   Username: {row['username']}")
    print(f"   Updated: {row['updated_at']}")
    print(f"\n   asset_quantities (raw):")
    raw_data = row['asset_quantities']
    print(f"   Tipo: {type(raw_data)}")
    print(f"   Conteúdo: {raw_data[:200] if raw_data else 'NULL'}...")
    
    if raw_data:
        parsed = json.loads(raw_data)
        print(f"\n   asset_quantities (parsed):")
        print(f"   {json.dumps(parsed, indent=2)}")

conn.close()

print("\n" + "="*80)
print("3️⃣ POSSÍVEIS CAUSAS DO PROBLEMA:")
print("-" * 80)

print("""
Se a quantidade ESTÁ no banco mas NÃO aparece na interface:

❌ CAUSA 1: Cache do Streamlit não foi limpo
   Solução:
   - Feche COMPLETAMENTE o Streamlit (Ctrl+C no terminal)
   - Execute novamente: streamlit run main.py
   - Faça login com 'hcarqueja'
   - Não clique em "Atualizar Cotações" ainda
   - Vá direto na seção "🇧🇷 FIIs Brasileiros"

❌ CAUSA 2: Session state do Streamlit está com dados antigos
   Solução:
   - No Streamlit, pressione a tecla 'C' no teclado
   - Ou menu ⋮ (três pontos) → "Clear cache"
   - Recarregue a página (F5)

❌ CAUSA 3: Variável ASSET_QUANTITIES não está sendo atualizada
   Solução:
   - O código carrega do banco na linha ~441 do main.py
   - Se você modificou depois de logar, precisa relogar

❌ CAUSA 4: O código está lendo de um local diferente
   Solução:
   - Verifique se há múltiplas instâncias do Streamlit rodando
   - Mate todos os processos Python e reinicie

═══════════════════════════════════════════════════════════════════════════

✅ SOLUÇÃO DEFINITIVA (PASSO A PASSO):

1. Pare o Streamlit:
   - Vá no terminal onde está rodando
   - Pressione Ctrl+C
   - Aguarde terminar completamente

2. Limpe o cache do Streamlit:
   - Delete a pasta: .streamlit/cache (se existir)
   - Ou execute: streamlit cache clear

3. Reinicie o Streamlit:
   - streamlit run main.py

4. Faça login NOVAMENTE:
   - Usuário: hcarqueja
   - Senha: 135678

5. Vá na barra lateral:
   - Procure por: "✅ X quantidades carregadas!"
   - Se aparecer "✅ 1 quantidades carregadas!", significa que carregou!
   - Clique em "🔍 Ver quantidades carregadas" para confirmar

6. Se aparecer, agora clique em "🔄 Atualizar Cotações"

7. Vá na seção "🇧🇷 FIIs Brasileiros"
   - Deve aparecer HGRE11.SA com 83 cotas

═══════════════════════════════════════════════════════════════════════════
""")

print("\n💡 Execute os passos acima e veja se resolve!")
print("="*80)
