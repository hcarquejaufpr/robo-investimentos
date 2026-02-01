import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from importlib import reload
import ssl
import hashlib
import config  # Importa suas configurações do config.py

# Desabilita verificação SSL (necessário em algumas redes corporativas)
ssl._create_default_https_context = ssl._create_unverified_context

# --- Configuração da Página ---
st.set_page_config(
    page_title="Robô Estratégia de Saída",
    page_icon="📈",
    layout="wide"
)

# ============================================================================
# SISTEMA DE AUTENTICAÇÃO MULTI-USUÁRIO
# ============================================================================

import json
import os

# ============================================================================
# GERENCIAMENTO DE CARTEIRAS POR USUÁRIO
# ============================================================================

def load_user_portfolio(username):
    """Carrega a carteira específica do usuário."""
    portfolios_file = "user_portfolios.json"
    
    # Carteira padrão (vazia)
    default_portfolio = {
        "US_STOCKS": [],
        "BR_FIIS": [],
        "TESOURO_DIRETO": {},
        "PARAMETROS": {
            "MULTIPLIER_US": 1.2,
            "MULTIPLIER_BR": 1.0
        }
    }
    
    if os.path.exists(portfolios_file):
        with open(portfolios_file, 'r') as f:
            portfolios = json.load(f)
            return portfolios.get(username, default_portfolio)
    
    return default_portfolio

def save_user_portfolio(username, portfolio):
    """Salva a carteira específica do usuário."""
    portfolios_file = "user_portfolios.json"
    
    # Carrega todas as carteiras
    if os.path.exists(portfolios_file):
        with open(portfolios_file, 'r') as f:
            portfolios = json.load(f)
    else:
        portfolios = {}
    
    # Atualiza a carteira do usuário
    portfolios[username] = portfolio
    
    # Salva
    with open(portfolios_file, 'w') as f:
        json.dump(portfolios, f, indent=2)

def load_users():
    """Carrega usuários do arquivo ou secrets."""
    try:
        # Tenta carregar do Streamlit secrets primeiro
        users_json = st.secrets.get("users", None)
        if users_json:
            return json.loads(users_json)
    except:
        pass
    
    # Se não existir, carrega do arquivo local
    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    
    # Usuário padrão se não existir nada
    return {
        "admin": {
            "password": "investidor2026",
            "name": "Administrador"
        }
    }

def save_users(users):
    """Salva usuários no arquivo local."""
    with open("users.json", 'w') as f:
        json.dump(users, f, indent=2)

def login_register_page():
    """Tela de login e registro."""
    
    st.markdown("""
    # 🤖 Robô de Investimentos
    ## Estratégia de Saída - Análise de Carteira
    """)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    # ========== ABA DE LOGIN ==========
    with tab1:
        st.subheader("Acesse sua conta")
        
        with st.form("login_form"):
            username = st.text_input("Usuário", key="login_username")
            password = st.text_input("Senha", type="password", key="login_password")
            submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            
            if submit:
                users = load_users()
                
                if username in users and users[username]["password"] == password:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["user_name"] = users[username]["name"]
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
    
    # ========== ABA DE CADASTRO ==========
    with tab2:
        st.subheader("Criar nova conta")
        
        with st.form("register_form"):
            new_username = st.text_input("Escolha um usuário", key="reg_username")
            new_name = st.text_input("Seu nome completo", key="reg_name")
            new_password = st.text_input("Escolha uma senha", type="password", key="reg_password")
            new_password2 = st.text_input("Confirme a senha", type="password", key="reg_password2")
            register = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)
            
            if register:
                # Validações
                if not new_username or not new_name or not new_password:
                    st.error("❌ Preencha todos os campos!")
                elif new_password != new_password2:
                    st.error("❌ As senhas não coincidem!")
                elif len(new_password) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres!")
                else:
                    users = load_users()
                    
                    if new_username in users:
                        st.error("❌ Este usuário já existe!")
                    else:
                        # Cria novo usuário
                        users[new_username] = {
                            "password": new_password,
                            "name": new_name
                        }
                        save_users(users)
                        st.success(f"✅ Conta criada com sucesso! Faça login com o usuário: {new_username}")
    
    st.markdown("---")
    st.caption("💡 **Usuário padrão:** admin | **Senha:** investidor2026")

def check_authentication():
    """Verifica se o usuário está autenticado."""
    
    # Se não estiver autenticado, mostra tela de login
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        login_register_page()
        return False
    
    return True

# Verifica autenticação antes de mostrar o app
if not check_authentication():
    st.stop()

# ============================================================================
# APP PRINCIPAL (só executa se autenticado)
# ============================================================================
# SISTEMA DE AUTENTICAÇÃO
# ============================================================================

def check_password():
    """Retorna True se o usuário está autenticado."""
    
    def password_entered():
        """Verifica se a senha está correta."""
        # Tenta pegar do secrets (Streamlit Cloud) ou usa padrão local
        try:
            correct_password = st.secrets["password"]
        except:
            # Senha padrão local: "investidor2026"
            # Hash SHA256 de "investidor2026"
            correct_password = "investidor2026"
        
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Remove senha da sessão
        else:
            st.session_state["password_correct"] = False

    # Primeira execução, mostra tela de login
    if "password_correct" not in st.session_state:
        st.markdown("""
        # 🔒 Área Restrita
        ## Robô de Investimentos - Estratégia de Saída
        
        Digite a senha para acessar seu dashboard de investimentos.
        """)
        
        st.text_input(
            "Senha de Acesso",
            type="password",
            on_change=password_entered,
            key="password",
            help="Senha padrão local: investidor2026"
        )
        
        st.info("💡 **Dica:** Configure sua senha personalizada em Settings > Secrets no Streamlit Cloud")
        return False
    
    # Senha incorreta
    elif not st.session_state["password_correct"]:
        st.markdown("""
        # 🔒 Área Restrita
        ## Robô de Investimentos - Estratégia de Saída
        """)
        
        st.text_input(
            "Senha de Acesso",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ Senha incorreta. Tente novamente.")
        return False
    
    # Senha correta
    else:
        return True

# Verifica autenticação antes de mostrar o app
if not check_authentication():
    st.stop()

# ============================================================================
# CARREGA CARTEIRA DO USUÁRIO LOGADO
# ============================================================================

# Obtém username do usuário logado
current_username = st.session_state.get("username", "admin")

# Carrega a carteira do usuário
user_portfolio = load_user_portfolio(current_username)

# Usa as configurações da carteira do usuário ao invés do config.py
US_STOCKS = user_portfolio.get("US_STOCKS", [])
BR_FIIS = user_portfolio.get("BR_FIIS", [])
TESOURO_DIRETO = user_portfolio.get("TESOURO_DIRETO", {})
PARAMETROS = user_portfolio.get("PARAMETROS", {"MULTIPLIER_US": 1.2, "MULTIPLIER_BR": 1.0})

# Multiplicadores individuais por ticker (opcional)
INDIVIDUAL_MULTIPLIERS = user_portfolio.get("INDIVIDUAL_MULTIPLIERS", {})

# ============================================================================
# APP PRINCIPAL (só executa se autenticado)
# ============================================================================

# Título e Cabeçalho com informações do usuário
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🤖 Painel de Estratégia de Saída (2026)")
with col2:
    st.markdown(f"### 👤 {st.session_state.get('user_name', 'Usuário')}")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("""
**Objetivo:** Vender ações e títulos nas próximas 3-4 semanas com o máximo de retorno.
* **Renda Variável:** Usa Volatilidade (ATR) para definir o preço de saída (Stop Loss).
* **Tesouro Direto:** Analisa a tabela regressiva de IR para economizar impostos.
""")

# --- Sidebar (Barra Lateral de Controles) ---
st.sidebar.header("⚙️ Painel de Controle")

# Mostra informações do usuário logado
st.sidebar.success(f"✅ Logado como: **{st.session_state.get('username', 'admin')}**")

# Mostra hora da última atualização
st.sidebar.caption(f"🕒 Atualizado: {datetime.now().strftime('%H:%M:%S')}")

# Sliders usando os valores padrão do seu config.py
mult_us = st.sidebar.slider(
    "🇺🇸 Stop Ações EUA (x ATR)", 
    1.0, 3.0, 
    float(PARAMETROS['MULTIPLIER_US']), 
    0.1,
    help="""📊 **Multiplicador do ATR para Stop Loss**
    
    • **ATR** = Average True Range (volatilidade média)
    • **Valores menores** (1.0-1.5x) = Stops mais próximos do preço → Mais sensível, vende mais rápido
    • **Valores maiores** (2.0-3.0x) = Stops mais distantes → Aguenta mais volatilidade
    
    💡 Para saída estratégica em 3-4 semanas, recomenda-se 1.0-1.5x"""
)

mult_br = st.sidebar.slider(
    "🇧🇷 Stop FIIs Brasil (x ATR)", 
    1.0, 3.0, 
    float(PARAMETROS['MULTIPLIER_BR']), 
    0.1,
    help="""📊 **Multiplicador do ATR para Stop Loss (FIIs)**
    
    • FIIs são geralmente menos voláteis que ações
    • **Valores menores** (1.0x) = Stops mais próximos → Proteção conservadora
    • **Valores maiores** (1.5-2.0x) = Stops mais distantes → Permite mais oscilação
    
    💡 FIIs tendem a ter ATR menor, então 1.0-1.5x é adequado"""
)

if st.sidebar.button("🔄 Atualizar Cotações", help="Recarrega os dados do mercado e limpa o cache. Use após salvar configurações ou para obter cotações mais recentes."):
    # Limpa o cache das funções
    st.cache_data.clear()
    # Força atualização da página
    st.rerun()

# --- Editor de Ativos ---
st.sidebar.markdown("---")
st.sidebar.header("📝 Gerenciar Ativos")

with st.sidebar.expander("🇺🇸 Ações Americanas", expanded=False):
    us_stocks_text = st.text_area(
        "Um ticker por linha (ex: AAPL)",
        value="\n".join(US_STOCKS),
        height=100,
        key="us_stocks",
        help="Digite os tickers das ações americanas, um por linha. Exemplos: AAPL, MSFT, NVDA, GOOGL, TSLA, AMZN"
    )

with st.sidebar.expander("🇧🇷 FIIs Brasileiros", expanded=False):
    br_fiis_text = st.text_area(
        "Um ticker por linha com .SA (ex: HGLG11.SA)",
        value="\n".join(BR_FIIS),
        height=100,
        key="br_fiis",
        help="Digite os códigos dos FIIs brasileiros com .SA no final. Exemplos: HGLG11.SA, MXRF11.SA, VISC11.SA, KNIP11.SA"
    )

with st.sidebar.expander("💰 Tesouro Direto", expanded=False):
    st.markdown("**Formato:** Nome | Data de Compra")
    st.caption("Exemplo: Tesouro Selic 2027 | 2024-02-15")
    
    tesouro_lines = []
    for nome, dados in TESOURO_DIRETO.items():
        tesouro_lines.append(f"{nome} | {dados['data_compra']}")
    
    tesouro_text = st.text_area(
        "Um título por linha",
        value="\n".join(tesouro_lines),
        height=100,
        key="tesouro",
        help="""💰 **Como preencher:**
        
        Formato: Nome do Título | Data de Compra (AAAA-MM-DD)
        
        Exemplos:
        • Tesouro Selic 2027 | 2024-02-15
        • Tesouro IPCA+ 2035 | 2023-01-10
        • Tesouro Prefixado 2029 | 2024-08-20
        
        O sistema calculará automaticamente a alíquota de IR e recomendará o melhor momento de venda."""
    )

# --- Ajustes Individuais de ATR ---
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Ajustes Individuais (Opcional)")

with st.sidebar.expander("🎯 Multiplicador ATR por Ativo", expanded=False):
    st.markdown("""
    **Personalize o stop de cada ativo individualmente!**
    
    Formato: `TICKER: multiplicador`
    
    Exemplos:
    ```
    AAPL: 1.5
    NVDA: 2.0
    HGLG11: 1.0
    ```
    
    Se não definir, usa o padrão (US ou BR).
    """)
    
    # Converte dicionário em texto editável
    individual_mult_lines = []
    for ticker, mult in INDIVIDUAL_MULTIPLIERS.items():
        individual_mult_lines.append(f"{ticker}: {mult}")
    
    individual_mult_text = st.text_area(
        "Multiplicadores personalizados",
        value="\n".join(individual_mult_lines),
        height=150,
        key="individual_mults",
        help="Deixe em branco para usar os multiplicadores padrão. Defina apenas os tickers que quer personalizar."
    )

if st.sidebar.button("💾 Salvar Configurações", type="primary", help="Salva sua carteira pessoal (ativos e parâmetros). Seus dados ficam separados de outros usuários."):
    try:
        # Processa ações americanas
        new_us_stocks = [line.strip() for line in us_stocks_text.split('\n') if line.strip()]
        
        # Processa FIIs brasileiros
        new_br_fiis = [line.strip() for line in br_fiis_text.split('\n') if line.strip()]
        
        # Processa Tesouro Direto
        new_tesouro = {}
        for line in tesouro_text.split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) == 2:
                    nome = parts[0].strip()
                    data = parts[1].strip()
                    new_tesouro[nome] = {'data_compra': data}
        
        # Processa multiplicadores individuais do text area (mantido por compatibilidade)
        new_individual_multipliers = {}
        for line in individual_mult_text.split('\n'):
            line = line.strip()
            if ':' in line:
                try:
                    ticker, mult = line.split(':', 1)
                    ticker = ticker.strip().upper()
                    mult = float(mult.strip())
                    if mult > 0:  # Valida multiplicador positivo
                        new_individual_multipliers[ticker] = mult
                except ValueError:
                    st.sidebar.warning(f"⚠️ Linha ignorada (formato inválido): {line}")
        
        # Captura edições das tabelas (prioridade sobre text area)
        if "edited_us" in st.session_state:
            for _, row in st.session_state["edited_us"].iterrows():
                ticker = row["Ticker"]
                mult = row["ATR Mult."]
                if pd.notna(mult) and mult > 0:
                    new_individual_multipliers[ticker] = float(mult)
        
        if "edited_br" in st.session_state:
            for _, row in st.session_state["edited_br"].iterrows():
                ticker = row["Ticker"]
                mult = row["ATR Mult."]
                if pd.notna(mult) and mult > 0:
                    new_individual_multipliers[ticker] = float(mult)
        
        # Cria o objeto de carteira do usuário
        user_portfolio = {
            "US_STOCKS": new_us_stocks,
            "BR_FIIS": new_br_fiis,
            "TESOURO_DIRETO": new_tesouro,
            "PARAMETROS": {
                "MULTIPLIER_US": mult_us,
                "MULTIPLIER_BR": mult_br
            },
            "INDIVIDUAL_MULTIPLIERS": new_individual_multipliers
        }
        
        # Salva a carteira específica deste usuário
        save_user_portfolio(current_username, user_portfolio)
        
        st.sidebar.success("✅ Sua carteira foi salva!")
        st.sidebar.info("Clique em 'Atualizar Cotações' para ver os novos dados")
        
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao salvar: {e}")

# --- Funções de Cálculo ---

@st.cache_data(ttl=300) # Cache de 5 minutos
def get_market_data(tickers, multiplier, individual_multipliers=None):
    """Baixa dados, calcula ATR, RSI e define Stop Loss."""
    if not tickers:
        return pd.DataFrame()
    
    if individual_multipliers is None:
        individual_multipliers = {}
    
    data_list = []
    errors = []
    
    # Barra de progresso visual
    bar = st.progress(0)
    status_text = st.empty()
    total = len(tickers)
    
    for i, ticker in enumerate(tickers):
        status_text.text(f"Baixando {ticker}... ({i+1}/{total})")
        try:
            # Usa Ticker.history() ao invés de yf.download()
            stock = yf.Ticker(ticker)
            df = stock.history(period="1y")
            
            if df.empty:
                errors.append(f"⚠️ {ticker}: Sem dados disponíveis (ticker inválido?)")
                bar.progress((i + 1) / total)
                continue
                
            # ================================================================
            # CÁLCULOS TÉCNICOS: ATR, SMA e RSI
            # ================================================================
            
            # 1. ATR (Average True Range) - Volatilidade
            df['High-Low'] = df['High'] - df['Low']
            df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
            df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
            df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
            df['ATR'] = df['TR'].rolling(window=14).mean()
            
            # 2. SMA (Simple Moving Average) - Tendência
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            
            # 3. RSI (Relative Strength Index) - Força Relativa
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Verifica se há dados suficientes
            if pd.isna(df['ATR'].iloc[-1]) or pd.isna(df['SMA_20'].iloc[-1]) or pd.isna(df['RSI'].iloc[-1]):
                errors.append(f"⚠️ {ticker}: Dados insuficientes para cálculo (precisa >20 dias)")
                bar.progress((i + 1) / total)
                continue
            
            # ================================================================
            # EXTRAÇÃO DOS VALORES FINAIS
            # ================================================================
            
            last_close = float(df['Close'].iloc[-1])
            last_atr = float(df['ATR'].iloc[-1])
            last_sma = float(df['SMA_20'].iloc[-1])
            last_rsi = float(df['RSI'].iloc[-1])
            
            # Usa multiplicador individual se existir, senão usa o padrão
            ticker_clean = ticker.replace(".SA", "")
            current_multiplier = individual_multipliers.get(ticker_clean, multiplier)
            
            # ================================================================
            # RSI TERMÔMETRO (Visual de Sobrecompra/Sobrevenda)
            # ================================================================
            
            if last_rsi >= 70:
                rsi_status = f"🔥 ALERTA: CARO ({last_rsi:.1f})"
                # LÓGICA INTELIGENTE: RSI > 70 = Sobrecomprado → Stop mais apertado automaticamente
                stop_multiplier = 1.0  # Proteção agressiva em topos
            elif last_rsi <= 30:
                rsi_status = f"❄️ Barato ({last_rsi:.1f})"
                stop_multiplier = current_multiplier  # Usa o multiplicador normal
            else:
                rsi_status = f"Neutro ({last_rsi:.1f})"
                stop_multiplier = current_multiplier  # Usa o multiplicador normal
            
            # ================================================================
            # CÁLCULO DE PREÇOS ESTRATÉGICOS
            # ================================================================
            
            # Stop Loss (Gatilho de Venda para limitar perdas)
            stop_price = last_close - (last_atr * stop_multiplier)
            
            # Take Profit / Alvo de Lucro (Projeção de alta baseada em volatilidade)
            # Usa 2.0x ATR para capturar movimentos significativos de alta
            gain_target = last_close + (last_atr * 2.0)
            
            # Potencial de Ganho até o alvo
            gain_potential_value = ((gain_target - last_close) / last_close) * 100
            
            # Tendência baseada na SMA
            tendencia = "🟢 Alta" if last_close > last_sma else "🔴 Baixa"
            
            # Aviso visual de contra-tendência (padrão do mercado)
            if last_close < last_sma:  # Tendência de baixa
                gain_potential_display = f"{gain_potential_value:.1f}% ⚠️"
            else:
                gain_potential_display = f"{gain_potential_value:.1f}%"
            
            # ATR como porcentagem do preço (mais prático para decisões)
            atr_percent = (last_atr / last_close) * 100
            
            # ================================================================
            # ADICIONA AO RESULTADO
            # ================================================================
            
            data_list.append({
                "Ticker": ticker_clean,
                "Preço Atual": last_close,
                "ATR %": atr_percent,  # Volatilidade percentual
                "RSI (Termômetro)": rsi_status,
                "Stop Loss Sugerido": stop_price,
                "Alvo (Gain)": gain_target,
                "Potencial": gain_potential_display,  # Com aviso visual
                "Distância Stop (%)": ((last_close - stop_price) / last_close) * 100,
                "ATR Mult.": current_multiplier,
                "Tendência": tendencia,
                "Histórico": df['Close'] # Salva para o gráfico
            })
            
        except Exception as e:
            errors.append(f"❌ {ticker}: {str(e)}")
            
        bar.progress((i + 1) / total)
        
    bar.empty()
    status_text.empty()
    
    # Mostra erros se houver
    if errors:
        with st.expander(f"⚠️ Problemas ao baixar {len(errors)} ticker(s)", expanded=True):
            for error in errors:
                st.warning(error)
    
    return pd.DataFrame(data_list)

def analyze_taxes(carteira):
    """Analisa dias regressivos do IR."""
    results = []
    hoje = datetime.now()
    
    for titulo, dados in carteira.items():
        compra = datetime.strptime(dados['data_compra'], "%Y-%m-%d")
        dias = (hoje - compra).days
        
        # Tabela Regressiva
        if dias <= 180:
            aliq, prox_aliq, dias_muda = 22.5, 20.0, 181 - dias
        elif dias <= 360:
            aliq, prox_aliq, dias_muda = 20.0, 17.5, 361 - dias
        elif dias <= 720:
            aliq, prox_aliq, dias_muda = 17.5, 15.0, 721 - dias
        else:
            aliq, prox_aliq, dias_muda = 15.0, 15.0, 0
            
        msg = "✅ Venda Liberada"
        cor = "green"
        
        if dias_muda > 0 and dias_muda <= 30:
            msg = f"🚨 AGUARDE {dias_muda} DIAS (Imposto cai de {aliq}% para {prox_aliq}%)"
            cor = "red"
        
        results.append({
            "Título": titulo,
            "Dias Investidos": dias,
            "Alíquota Hoje": f"{aliq}%",
            "Status": msg,
            "Cor": cor
        })
    return pd.DataFrame(results)

# --- EXECUÇÃO DO LAYOUT ---

# 1. Análise de Ações e FIIs
st.header("📊 Renda Variável: Ações e FIIs")

# Explicação dos indicadores
with st.expander("❓ Como interpretar a tabela", expanded=False):
    st.markdown("""
    ### 📖 Guia de Leitura da Análise Completa
    
    **🎯 Preço Atual:** Último preço de fechamento do ativo
    
    ---
    
    ### 📊 O que é ATR (Average True Range)?
    
    **ATR = Volatilidade Média do Ativo nos últimos 14 dias**
    
    É um indicador técnico que mede o quanto o preço do ativo costuma variar diariamente:
    - **ATR Alto** → Ativo volátil (oscila muito). Ex: ações de tecnologia, small caps
    - **ATR Baixo** → Ativo estável (oscila pouco). Ex: FIIs, empresas consolidadas
    
    **Por que usar ATR?**
    - **Stops Inteligentes:** Em vez de usar valores fixos ($5, $10), o stop se adapta à volatilidade do ativo
    - **Comparação Justa:** Um stop de "1.0x ATR" significa "1 oscilação normal" para qualquer ativo
    - **Evita Falsos Sinais:** Stops muito apertados em ativos voláteis causam vendas desnecessárias
    
    **Exemplo Prático:**
    - AAPL com ATR de $5 → Stop em 1.2x ATR = $6 de folga
    - FII com ATR de R$0.50 → Stop em 1.0x ATR = R$0.50 de folga
    
    ---
    
    **🌡️ RSI (Termômetro):**
    - 🔥 **ALERTA: CARO (≥70)** → Ativo em sobrecompra, possível topo. **AUTOMÁTICO:** Stop ajustado para 1.0x ATR (proteção de lucro).
    - ❄️ **Barato (≤30)** → Ativo em sobrevenda, possível fundo. Oportunidade de compra (se tendência favorável).
    - **Neutro (31-69)** → Zona normal, sem extremos.
    
    **🛑 Stop Loss:** Preço de venda automática para limitar perdas (calculado com ATR × multiplicador). 
    - Fórmula: `Stop = Preço Atual - (ATR × Multiplicador)`
    - RSI > 70? Sistema ajusta para 1.0x ATR automaticamente (proteção agressiva em topos).
    
    **🎯 Alvo (Gain):** Meta de lucro projetada baseada em volatilidade.
    - Fórmula: `Alvo = Preço Atual + (ATR × 2.0)`
    - Projeta um movimento de alta equivalente a 2 oscilações normais do ativo.
    
    **📈 Potencial:** Ganho percentual esperado se atingir o alvo.
    - **Sem aviso:** Alvo alinhado com tendência de alta (ex: `4.5%`)
    - **Com ⚠️:** Alvo contra tendência de baixa (ex: `6.7% ⚠️`) - Operação mais arriscada, requer reversão
    - Compare com "Risco (%)" para avaliar relação risco/retorno.
    
    **⚠️ Risco (%):** Distância percentual até o stop loss (quanto pode cair antes de acionar a venda).
    
    **📈 Tendência (SMA 20 dias):** 
    - 🟢 **Alta** → Preço acima da média móvel dos últimos 20 dias. Momento ascendente.
    - 🔴 **Baixa** → Preço abaixo da média móvel. Momento descendente.
    
    **⚙️ ATR Mult.:** Multiplicador editável. Clique duplo para personalizar o stop de cada ativo individualmente.
    - Conservador: 0.5x - 1.0x (stops mais apertados)
    - Moderado: 1.2x - 1.5x (equilíbrio)
    - Agressivo: 2.0x - 3.0x (stops mais largos, maior tolerância)
    """)

# Ações Americanas
st.subheader("🇺🇸 Ações Americanas")
st.caption("💡 **Dica:** RSI > 70 ativa stop automático em 1.0x ATR (proteção de lucro). Edite 'ATR Mult.' para personalizar.")
if US_STOCKS:
    st.caption(f"📊 Analisando {len(US_STOCKS)} ticker(s): {', '.join(US_STOCKS)}")
    df_us = get_market_data(US_STOCKS, mult_us, individual_multipliers=INDIVIDUAL_MULTIPLIERS)
    if not df_us.empty:
        # Configura colunas editáveis
        edited_df_us = st.data_editor(
            df_us[["Ticker", "Preço Atual", "ATR %", "RSI (Termômetro)", "Stop Loss Sugerido", "Alvo (Gain)", "Potencial", "Distância Stop (%)", "Tendência", "ATR Mult."]],
            use_container_width=True,
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", disabled=True),
                "Preço Atual": st.column_config.NumberColumn(
                    "Preço Atual",
                    format="$%.1f",
                    disabled=True
                ),
                "ATR %": st.column_config.NumberColumn(
                    "Volatilidade (ATR) %",
                    format="%.1f%%",
                    help="Oscilação diária média. <2% = estável, 2-5% = moderado, >5% = volátil.",
                    disabled=True
                ),
                "RSI (Termômetro)": st.column_config.TextColumn("RSI (Termômetro)", disabled=True),
                "Stop Loss Sugerido": st.column_config.NumberColumn(
                    "Stop Loss 🛑",
                    format="$%.1f",
                    help="Preço de venda automática para limitar perdas. RSI > 70 ajusta para 1.0x ATR.",
                    disabled=True
                ),
                "Alvo (Gain)": st.column_config.NumberColumn(
                    "Alvo (Gain) 🎯",
                    format="$%.1f",
                    help="Preço alvo de lucro (2.0x ATR acima do preço atual). Meta de venda estratégica.",
                    disabled=True
                ),
                "Potencial": st.column_config.TextColumn(
                    "Potencial 📈",
                    help="Ganho % se atingir o alvo. ⚠️ = Contra tendência de baixa (operação mais arriscada).",
                    disabled=True
                ),
                "Distância Stop (%)": st.column_config.NumberColumn(
                    "Risco (%)",
                    format="%.1f%%",
                    help="Distância percentual até o stop loss (quanto pode cair antes de vender).",
                    disabled=True
                ),
                "Tendência": st.column_config.TextColumn("Tendência", disabled=True),
                "ATR Mult.": st.column_config.NumberColumn(
                    "ATR Mult. ⚙️",
                    help="Multiplicador do ATR para calcular o stop loss. Clique duplo para editar!",
                    min_value=0.1,
                    max_value=5.0,
                    step=0.1,
                    format="%.1fx",
                    required=True,
                ),
            },
            num_rows="fixed",
            hide_index=True,
            key="editor_us"
        )
        # Armazena no session_state para salvar depois
        st.session_state["edited_us"] = edited_df_us
    else:
        st.warning("Nenhum dado disponível para ações americanas")
else:
    st.info("Adicione tickers em config.py")

st.markdown("---")  # Separador visual

# FIIs Brasileiros
st.subheader("🇧🇷 FIIs Brasileiros")
st.caption("💡 **Dica:** RSI > 70 ativa stop automático em 1.0x ATR (proteção de lucro). Edite 'ATR Mult.' para personalizar.")
if BR_FIIS:
    st.caption(f"📊 Analisando {len(BR_FIIS)} ticker(s): {', '.join(BR_FIIS)}")
    df_br = get_market_data(BR_FIIS, mult_br, individual_multipliers=INDIVIDUAL_MULTIPLIERS)
    if not df_br.empty:
        # Configura colunas editáveis
        edited_df_br = st.data_editor(
            df_br[["Ticker", "Preço Atual", "ATR %", "RSI (Termômetro)", "Stop Loss Sugerido", "Alvo (Gain)", "Potencial", "Distância Stop (%)", "Tendência", "ATR Mult."]],
            use_container_width=True,
            column_config={
                "Ticker": st.column_config.TextColumn("Ticker", disabled=True),
                "Preço Atual": st.column_config.NumberColumn(
                    "Preço Atual",
                    format="R$ %.1f",
                    disabled=True
                ),
                "ATR %": st.column_config.NumberColumn(
                    "Volatilidade (ATR) %",
                    format="%.1f%%",
                    help="Oscilação diária média. <2% = estável, 2-5% = moderado, >5% = volátil.",
                    disabled=True
                ),
                "RSI (Termômetro)": st.column_config.TextColumn("RSI (Termômetro)", disabled=True),
                "Stop Loss Sugerido": st.column_config.NumberColumn(
                    "Stop Loss 🛑",
                    format="R$ %.1f",
                    help="Preço de venda automática para limitar perdas. RSI > 70 ajusta para 1.0x ATR.",
                    disabled=True
                ),
                "Alvo (Gain)": st.column_config.NumberColumn(
                    "Alvo (Gain) 🎯",
                    format="R$ %.1f",
                    help="Preço alvo de lucro (2.0x ATR acima do preço atual). Meta de venda estratégica.",
                    disabled=True
                ),
                "Potencial": st.column_config.TextColumn(
                    "Potencial 📈",
                    help="Ganho % se atingir o alvo. ⚠️ = Contra tendência de baixa (operação mais arriscada).",
                    disabled=True
                ),
                "Distância Stop (%)": st.column_config.NumberColumn(
                    "Risco (%)",
                    format="%.1f%%",
                    help="Distância percentual até o stop loss (quanto pode cair antes de vender).",
                    disabled=True
                ),
                "Tendência": st.column_config.TextColumn("Tendência", disabled=True),
                "ATR Mult.": st.column_config.NumberColumn(
                    "ATR Mult. ⚙️",
                    help="Multiplicador do ATR para calcular o stop loss. Clique duplo para editar!",
                    min_value=0.1,
                    max_value=5.0,
                    step=0.1,
                    format="%.1fx",
                    required=True,
                ),
            },
            num_rows="fixed",
            hide_index=True,
            key="editor_br"
        )
        # Armazena no session_state para salvar depois
        st.session_state["edited_br"] = edited_df_br
    else:
        st.warning("Nenhum dado disponível para FIIs")
else:
    st.info("Adicione FIIs em config.py")

# 2. Otimização Fiscal
st.header("💰 Tesouro Direto: Análise de IR")

# Explicação da tabela regressiva
with st.expander("❓ Como funciona a tributação do Tesouro Direto", expanded=False):
    st.markdown("""
    ### 📖 Tabela Regressiva de IR
    
    O Imposto de Renda sobre o Tesouro Direto **diminui com o tempo:**
    
    | Período Investido | Alíquota de IR |
    |-------------------|----------------|
    | Até 180 dias      | 22,5% 😰       |
    | 181 a 360 dias    | 20,0% 😐       |
    | 361 a 720 dias    | 17,5% 😊       |
    | Acima de 720 dias | 15,0% 😃       |
    
    ### 💡 Estratégia de Otimização
    
    - 🚨 **AGUARDE** → Se faltam menos de 30 dias para a próxima faixa, vale a pena esperar!
    - ✅ **Pode vender** → Se está longe da próxima mudança ou já está na menor alíquota (15%).
    
    **Exemplo:** Um título com 355 dias investidos está a apenas 6 dias de cair de 20% para 17,5%. 
    Esperar economiza 2,5% do rendimento!
    """)

if TESOURO_DIRETO:
    df_tesouro = analyze_taxes(TESOURO_DIRETO)
    
    for _, row in df_tesouro.iterrows():
        if row['Cor'] == 'red':
            st.error(f"**{row['Título']}** - {row['Status']}")
        else:
            st.success(f"**{row['Título']}** - {row['Status']}")
    
    st.dataframe(
        df_tesouro[["Título", "Dias Investidos", "Alíquota Hoje", "Status"]],
        use_container_width=True
    )
else:
    st.info("Adicione títulos do Tesouro Direto em config.py")

# 3. Rodapé
st.markdown("---")
st.caption("📅 Dados atualizados automaticamente. Cache de 5 minutos.")