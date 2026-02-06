# Análise de Bitcoin - Documentação

## 🎯 Funcionalidade

A aplicação agora inclui análise técnica completa do Bitcoin (BTC-USD) com:

- **Preço atual** e variações (dia, semana, mês)
- **Indicadores técnicos**: RSI, MACD, Médias Móveis, Bandas de Bollinger
- **Sinais de trading**: Análise automatizada indicando compra, venda ou neutro
- **Score de recomendação**: Pontuação de -100 (venda forte) a +100 (compra forte)
- **Tendência**: Identificação da direção do mercado
- **Gráfico interativo**: Visualização com candlesticks e médias móveis

## 📊 Indicadores Incluídos

### RSI (Relative Strength Index)
- **< 30**: Sobrevendido (possível oportunidade de compra)
- **30-70**: Zona neutra
- **> 70**: Sobrecomprado (possível correção)

### MACD (Moving Average Convergence Divergence)
- Identifica mudanças no momentum
- Cruzamento da linha MACD com a linha de sinal indica reversão

### Médias Móveis (SMA)
- **MM 20**: Curto prazo
- **MM 50**: Médio prazo
- **MM 200**: Longo prazo
- **Golden Cross**: MM50 > MM200 (sinal de alta)
- **Death Cross**: MM50 < MM200 (sinal de baixa)

### Bandas de Bollinger
- Indica níveis de sobrecompra/sobrevenda
- Preço próximo da banda inferior: possível compra
- Preço próximo da banda superior: possível venda

### Volume
- Compara volume atual com média de 20 dias
- Alto volume confirma movimentos

## 🚀 Como Usar

1. **Acesse a aplicação**:
   ```bash
   streamlit run main.py
   ```

2. **Faça login** com seu usuário e senha

3. **Visualize a análise de Bitcoin** na primeira seção da página

4. **Interprete os sinais**:
   - 🟢🟢 **COMPRA FORTE**: Score > 40, múltiplos indicadores favoráveis
   - 🟢 **COMPRA**: Score > 15, indicadores moderadamente favoráveis
   - 🟡 **NEUTRO**: Score entre -15 e 15, sem direção clara
   - 🔴 **VENDA**: Score < -15, indicadores moderadamente desfavoráveis
   - 🔴🔴 **VENDA FORTE**: Score < -40, múltiplos indicadores desfavoráveis

5. **Analise a tendência**:
   - 📈📈 **ALTA FORTE**: Variação mensal > 10% e semanal > 5%
   - 📈 **ALTA**: Variações positivas
   - ➡️ **LATERAL**: Sem direção clara
   - 📉 **BAIXA**: Variações negativas
   - 📉📉 **BAIXA FORTE**: Variação mensal < -10% e semanal < -5%

## 🔧 Arquivos Criados

- **analise_bitcoin.py**: Módulo principal com todas as funções de análise
- **test_bitcoin_analise.py**: Script de teste da funcionalidade
- **ANALISE_BITCOIN.md**: Esta documentação

## ⚠️ Problemas de SSL

Se encontrar erros de certificado SSL:

### Solução 1: Variáveis de Ambiente (Windows PowerShell)
```powershell
$env:PYTHONHTTPSVERIFY="0"
$env:CURL_CA_BUNDLE=""
streamlit run main.py
```

### Solução 2: Variáveis de Ambiente (Windows CMD)
```cmd
set PYTHONHTTPSVERIFY=0
set CURL_CA_BUNDLE=
streamlit run main.py
```

### Solução 3: No Streamlit Cloud
Adicione ao `config.toml`:
```toml
[server]
enableXsrfProtection = false
enableCORS = false
```

### Solução 4: Atualizar yfinance
```bash
pip install --upgrade yfinance
```

## 📈 Exemplo de Análise

```
₿ Análise de Bitcoin (BTC-USD)

💵 Preço Atual: $47,523.45 (+2.34%)
📊 Var. 7 dias: +5.67% 📈
📈 Var. 30 dias: +12.45% 📈
🎯 Recomendação: COMPRA FORTE (Score: 65/100)

Indicadores Técnicos:
- RSI: 58.3 (Zona neutra)
- MACD: 234.56 (Sinal: 198.23)
- MM 20: $45,123 (+5.32%)
- MM 50: $43,567 (+9.08%)
- MM 200: $41,234 (+15.25%)

Sinais de Trading:
✅ RSI: NEUTRO (Valor: 58.3)
✅ MACD: COMPRA MODERADA (Histograma: 36.33)
✅ Médias Móveis: COMPRA FORTE (Acima MM50 e MM200)
✅ Bollinger: NEUTRO
```

## 🎯 Estratégias Sugeridas

### Compra Forte (Score > 40)
- Entrada em posição ou aumento de exposição
- Stop loss na banda inferior de Bollinger
- Alvo de curto prazo na banda superior

### Compra Moderada (Score 15-40)
- Entrada gradual em posição
- Aguardar confirmação de tendência
- Usar stop loss apertado

### Neutro (Score -15 a 15)
- Aguardar sinais mais claros
- Manter posições atuais se existentes
- Observar rompimentos de suporte/resistência

### Venda Moderada (Score -40 a -15)
- Realizar lucros parciais
- Apertar stops de proteção
- Reduzir exposição temporariamente

### Venda Forte (Score < -40)
- Realização de lucros ou saída de posição
- Aguardar correção para novas entradas
- Proteção de capital é prioridade

## 📝 Notas Importantes

1. **Análise técnica não é garantia**: Os indicadores são ferramentas de análise, não previsões
2. **Gerencie riscos**: Sempre use stop loss e não invista mais do que pode perder
3. **Diversifique**: Bitcoin é volátil, não concentre todo capital em um ativo
4. **Atualizações**: Dados são atualizados em tempo real via Yahoo Finance
5. **Cache**: Sistema tem cache de 5 minutos para economizar requisições

## 🔄 Futuras Melhorias

- [ ] Alertas automáticos por email quando há sinais fortes
- [ ] Análise de outras criptomoedas (ETH, BNB, etc.)
- [ ] Backtesting de estratégias
- [ ] Análise de correlação com mercado tradicional
- [ ] Suporte e resistência automáticos
- [ ] Análise de padrões gráficos (candlestick patterns)

## 📞 Suporte

Em caso de dúvidas ou problemas:
1. Verifique a configuração SSL
2. Atualize yfinance: `pip install --upgrade yfinance`
3. Verifique conexão de internet
4. Teste com o script `test_bitcoin_analise.py`

---

**Desenvolvido para Robô de Investimentos - 2026**
