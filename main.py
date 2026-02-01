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
if not check_password():
    st.stop()

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
    float(config.PARAMETROS['MULTIPLIER_US']), 
    0.1
)

mult_br = st.sidebar.slider(
    "🇧🇷 Stop FIIs Brasil (x ATR)", 
    1.0, 3.0, 
    float(config.PARAMETROS['MULTIPLIER_BR']), 
    0.1
)

if st.sidebar.button("🔄 Atualizar Cotações"):
    # Recarrega o módulo config
    reload(config)
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
        value="\n".join(config.US_STOCKS),
        height=100,
        key="us_stocks"
    )

with st.sidebar.expander("🇧🇷 FIIs Brasileiros", expanded=False):
    br_fiis_text = st.text_area(
        "Um ticker por linha com .SA (ex: HGLG11.SA)",
        value="\n".join(config.BR_FIIS),
        height=100,
        key="br_fiis"
    )

with st.sidebar.expander("💰 Tesouro Direto", expanded=False):
    st.markdown("**Formato:** Nome | Data de Compra")
    st.caption("Exemplo: Tesouro Selic 2027 | 2024-02-15")
    
    tesouro_lines = []
    for nome, dados in config.TESOURO_DIRETO.items():
        tesouro_lines.append(f"{nome} | {dados['data_compra']}")
    
    tesouro_text = st.text_area(
        "Um título por linha",
        value="\n".join(tesouro_lines),
        height=100,
        key="tesouro"
    )

if st.sidebar.button("💾 Salvar Configurações", type="primary"):
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
        
        # Gera o novo conteúdo do config.py
        config_content = f'''"""
Arquivo de Configuração do Robô de Investimentos
================================================
Altere os tickers e datas conforme sua carteira real.
"""

# ============================================================================
# AÇÕES AMERICANAS
# ============================================================================
US_STOCKS = {new_us_stocks}

# ============================================================================
# FUNDOS IMOBILIÁRIOS BRASILEIROS (FIIs)
# ============================================================================
BR_FIIS = {new_br_fiis}

# ============================================================================
# TESOURO DIRETO
# ============================================================================
TESOURO_DIRETO = {new_tesouro}

# ============================================================================
# PARÂMETROS DE ANÁLISE TÉCNICA
# ============================================================================
PARAMETROS = {{
    'MULTIPLIER_US': {mult_us},
    'MULTIPLIER_BR': {mult_br},
}}
'''
        
        # Salva o arquivo
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        # RECARREGA o módulo config
        reload(config)
        
        st.sidebar.success("✅ Configurações salvas e recarregadas!")
        st.sidebar.info("Clique em 'Atualizar Cotações' para ver os novos dados")
        
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao salvar: {e}")

# --- Funções de Cálculo ---

@st.cache_data(ttl=300) # Cache de 5 minutos
def get_market_data(tickers, multiplier):
    """Baixa dados, calcula ATR e define Stop Loss."""
    if not tickers:
        return pd.DataFrame()
    
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
                
            # Cálculos Matemáticos (ATR e Tendência)
            df['High-Low'] = df['High'] - df['Low']
            df['High-PrevClose'] = abs(df['High'] - df['Close'].shift(1))
            df['Low-PrevClose'] = abs(df['Low'] - df['Close'].shift(1))
            df['TR'] = df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
            
            # ATR de 14 dias
            df['ATR'] = df['TR'].rolling(window=14).mean()
            
            # Média Móvel de 20 dias (Tendência)
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            
            # Verifica se há dados suficientes
            if pd.isna(df['ATR'].iloc[-1]) or pd.isna(df['SMA_20'].iloc[-1]):
                errors.append(f"⚠️ {ticker}: Dados insuficientes para cálculo (precisa >20 dias)")
                bar.progress((i + 1) / total)
                continue
            
            # Dados finais
            last_close = float(df['Close'].iloc[-1])
            last_atr = float(df['ATR'].iloc[-1])
            last_sma = float(df['SMA_20'].iloc[-1])
            
            # Preço de Stop (Gatilho de Venda)
            stop_price = last_close - (last_atr * multiplier)
            
            tendencia = "🟢 Alta" if last_close > last_sma else "🔴 Baixa"
            
            data_list.append({
                "Ticker": ticker.replace(".SA", ""),
                "Preço Atual": last_close,
                "Stop Loss Sugerido": stop_price,
                "Distância (%)": ((last_close - stop_price) / last_close) * 100,
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

col1, col2 = st.columns(2)

with col1:
    st.subheader("🇺🇸 Ações Americanas")
    if config.US_STOCKS:
        st.caption(f"📊 Analisando {len(config.US_STOCKS)} ticker(s): {', '.join(config.US_STOCKS)}")
        df_us = get_market_data(config.US_STOCKS, mult_us)
        if not df_us.empty:
            st.dataframe(
                df_us[["Ticker", "Preço Atual", "Stop Loss Sugerido", "Distância (%)", "Tendência"]],
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado disponível para ações americanas")
    else:
        st.info("Adicione tickers em config.py")

with col2:
    st.subheader("🇧🇷 FIIs Brasileiros")
    if config.BR_FIIS:
        st.caption(f"📊 Analisando {len(config.BR_FIIS)} ticker(s): {', '.join(config.BR_FIIS)}")
        df_br = get_market_data(config.BR_FIIS, mult_br)
        if not df_br.empty:
            st.dataframe(
                df_br[["Ticker", "Preço Atual", "Stop Loss Sugerido", "Distância (%)", "Tendência"]],
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado disponível para FIIs")
    else:
        st.info("Adicione FIIs em config.py")

# 2. Otimização Fiscal
st.header("💰 Tesouro Direto: Análise de IR")

if config.TESOURO_DIRETO:
    df_tesouro = analyze_taxes(config.TESOURO_DIRETO)
    
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