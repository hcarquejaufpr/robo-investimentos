"""
Script para testar se o salvamento de quantidades pela interface funciona
"""
print("""
================================================================================
TESTE: SALVAMENTO DE QUANTIDADES PELA INTERFACE
================================================================================

Para testar se a interface funciona corretamente:

1. Execute: streamlit run main.py
2. Faça login com 'hcarqueja'
3. Na barra lateral:
   
   a) Expanda "📊 Quantidades de Ativos"
   
   b) Expanda "🇧🇷 Quantidades Brasil"
      - Você verá: HGRE11.SA | 83
   
   c) Clique na célula da quantidade (83)
      - Mude para outro valor (ex: 85)
      - Pressione ENTER
   
   d) ROLE PARA BAIXO na barra lateral
   
   e) Expanda "💾 Salvar Quantidades"
      - Clique em "💾 SALVAR QUANTIDADES AGORA"
   
   f) Aguarde a mensagem: "✅ X quantidade(s) salva(s)!"

4. Depois execute este verificador:

""")

import database as db

username = 'hcarqueja'
portfolio = db.load_user_portfolio(username)

if portfolio and 'ASSET_QUANTITIES' in portfolio:
    quantities = portfolio['ASSET_QUANTITIES']
    print(f"📊 Quantidades atuais no banco:")
    for ticker, qty in quantities.items():
        if isinstance(qty, dict):
            print(f"   • {ticker}: {qty.get('quantidade', 0)} cotas")
        else:
            print(f"   • {ticker}: {qty} cotas")
    
    hgre_qty = quantities.get('HGRE11.SA', {})
    if isinstance(hgre_qty, dict):
        current = hgre_qty.get('quantidade', 0)
    else:
        current = hgre_qty
    
    print(f"\n✅ Quantidade atual de HGRE11.SA: {current}")
    print(f"\n💡 Se você mudou para 85, deveria aparecer 85 aqui.")
    print(f"   Se ainda está 83, o salvamento pela interface NÃO funcionou.")
else:
    print("❌ Nenhuma quantidade encontrada")

print("\n" + "="*80)
print("POSSÍVEIS PROBLEMAS:")
print("="*80)
print("""
1. BOTÃO DIFÍCIL DE ENCONTRAR:
   - O botão "💾 SALVAR QUANTIDADES AGORA" está DENTRO de outro expander
   - Usuários podem não perceber que precisam EXPANDIR e depois CLICAR

2. FEEDBACK VISUAL INSUFICIENTE:
   - A tabela muda visualmente quando você edita
   - MAS não há indicação clara de que é preciso SALVAR depois

3. SOLUÇÃO:
   - Tornar o botão de salvar mais visível
   - Ou adicionar auto-save quando sair da célula
   - Ou mostrar badge "NÃO SALVO" quando houver mudanças pendentes
""")
