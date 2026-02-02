# 🎯 Preços de Stop Loss e Stop Gain

## 📊 O Que São Essas Colunas?

O sistema agora mostra 4 valores calculados automaticamente para você usar no seu home broker:

### 🛑 Stop Loss (Proteção)
- **🛑 SL Disparo**: Preço que ativa a ordem de venda
- **🛑 SL Limite**: Preço mínimo de venda (0.5% abaixo do disparo)

### 💰 Stop Gain (Lucro)
- **💰 SG Disparo**: Preço que realiza lucro automaticamente
- **💰 SG Limite**: Preço mínimo após ativar (0.5% abaixo do disparo)

---

## 💡 Como Usar no Seu Home Broker

### Exemplo: TGAR11

Suponha que na tabela você vê:
- Preço Atual: R$ 10,00
- 🛑 SL Disparo: R$ 9,50
- 🛑 SL Limite: R$ 9,45
- 💰 SG Disparo: R$ 11,00
- 💰 SG Limite: R$ 10,95

### Criar Stop Loss (Proteger contra quedas)

1. Acesse seu home broker (Clear, Rico, XP, etc.)
2. Selecione TGAR11.SA
3. Escolha: **Ordem de Stop Loss**
4. Configure:
   - **Preço de Disparo**: R$ 9,50
   - **Preço Limite**: R$ 9,45
   - **Quantidade**: quantas cotas quer proteger
5. Confirme

**Resultado**: Se o preço cair para R$ 9,50, vende automaticamente por no mínimo R$ 9,45

### Criar Stop Gain (Realizar lucro)

1. Acesse seu home broker
2. Selecione TGAR11.SA
3. Escolha: **Ordem de Stop Gain** (ou Stop de Venda)
4. Configure:
   - **Preço de Disparo**: R$ 11,00
   - **Preço Limite**: R$ 10,95
   - **Quantidade**: quantas cotas quer vender
5. Confirme

**Resultado**: Se o preço subir para R$ 11,00, vende automaticamente por no mínimo R$ 10,95

---

## 📋 Regras Importantes

### Disparo vs Limite

**Sempre**: Preço de Disparo > Preço Limite

- **Disparo**: Preço que "liga" a ordem
- **Limite**: Preço mínimo que você aceita vender

### Margem de Segurança

O sistema usa margem de 0.5% entre disparo e limite para:
- ✅ Garantir execução da ordem
- ✅ Evitar rejeição por falta de liquidez
- ✅ Proteger em momentos de volatilidade

---

## 🔄 Atualizações

Os valores são recalculados automaticamente quando você clica em **"🔄 Atualizar Cotações"**:

- **Stop Loss**: Baseado no ATR (volatilidade)
- **Stop Gain**: Baseado no preço alvo (2x ATR acima)
- **Margens**: Sempre 0.5% de diferença

---

## ⚙️ Personalização

Você pode ajustar os multiplicadores ATR na barra lateral:
- **🇺🇸 Stop Ações EUA**: 1.0 - 3.0x ATR
- **🇧🇷 Stop FIIs Brasil**: 1.0 - 3.0x ATR

Isso ajusta automaticamente os valores de Stop Loss e consequentemente as 4 colunas.

---

## 💡 Dicas por Tipo de Ativo

### FIIs (Fundos Imobiliários)
- Use os valores sugeridos como estão
- Liquidez menor = margem de 0.5% é adequada
- Considere ordens com validade maior (30 dias+)

### Ações US (Alta Liquidez)
- Valores funcionam bem como sugerido
- Pode reduzir margem para 0.2-0.3% se preferir
- Execução geralmente rápida

### Ativos Voláteis
- Se ATR % > 5%, considere margem maior (1%)
- Proteja-se de oscilações bruscas

---

## ❓ Perguntas Frequentes

### O sistema executa as vendas automaticamente?

**NÃO**. O sistema apenas CALCULA os valores. Você precisa:
1. Copiar os valores da tabela
2. Acessar seu home broker
3. Criar as ordens manualmente

### Preciso criar ambos Stop Loss e Stop Gain?

Não. Você pode criar:
- ✅ Apenas Stop Loss (proteção)
- ✅ Apenas Stop Gain (lucro)
- ✅ Ambos (proteção + lucro)

### Os valores mudam?

Sim! A cada atualização, os valores são recalculados baseados no preço atual e volatilidade recente.

### Posso ajustar os valores?

Sim! Os valores são sugestões. Você pode:
- Usar como estão
- Ajustar conforme sua estratégia
- Modificar multiplicadores ATR

---

## 🚀 Fluxo Recomendado

1. **Abra o sistema** → Clique em "🔄 Atualizar Cotações"
2. **Analise a tabela** → Veja os 4 valores para cada ativo
3. **Acesse home broker** → Entre na sua corretora
4. **Copie os valores** → Use exatamente como mostrado
5. **Crie as ordens** → Configure Stop Loss e/ou Stop Gain
6. **Monitore diariamente** → Atualize e ajuste conforme necessário

---

**Simples e Prático! 📈**
