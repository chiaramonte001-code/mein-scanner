import streamlit as st
import requests
import pandas as pd

# --- DEIN SETUP ---
GEHEIM_CODE = "PRO-2025"
BEZAHL_LINK = "https://paypal.me/DEINNAME/5"

st.set_page_config(page_title="Crypto AI Scanner", page_icon="⚡", layout="wide")

# --- LOGIN ---
with st.sidebar:
    st.header("🔐 Login")
    passwort = st.text_input("Code eingeben:", type="password")
    
    if passwort != GEHEIM_CODE:
        st.warning("Zugriff verweigert")
        st.markdown(f"👉 **[Zugang kaufen (5 CHF)]({BEZAHL_LINK})**")
        st.stop()
    else:
        st.success("Pro-Modus Aktiv")

# --- HAUPT TOOL ---
st.title("⚡ Crypto AI Scanner Pro")
st.markdown("Scanne den gesamten Markt nach unterbewerteten Coins.")

if st.button("🚀 JETZT SCANNEN"):
    with st.spinner("Lade Live-Daten..."):
        try:
            # 1. Daten holen
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 20,
                "page": 1,
                "sparkline": "false"
            }
            # Timeout erhöht für Stabilität
            res = requests.get(url, params=params, timeout=15)
            
            if res.status_code != 200:
                st.error(f"API Fehler: {res.status_code}. Versuche es in 1 Minute erneut.")
            else:
                data = res.json()
                
                # 2. Daten verarbeiten
                results = []
                for coin in 
                    # Signal Logik
                    change = coin.get('price_change_percentage_24h', 0)
                    if change is None: change = 0
                    
                    signal = "⚪ NEUTRAL"
                    if change < -5:
                        signal = "🟢 STRONG BUY"
                    elif change < -2:
                        signal = "🟢 BUY"
                    elif change > 5:
                        signal = "🔴 STRONG SELL"
                    elif change > 2:
                        signal = "🔴 SELL"
                    
                    results.append({
                        "Coin": coin['name'],
                        "Preis ($)": coin['current_price'],
                        "24h %": f"{change:.2f}%",
                        "SIGNAL": signal
                    })

                # 3. Tabelle anzeigen
                df = pd.DataFrame(results)
                
                # Beste Signale filtern
                st.subheader("💎 Beste Signale")
                st.dataframe(df)

        except Exception as e:
            st.error(f"Ein Fehler ist aufgetreten: {e}")

else:
    st.info("Klicke den Button zum Starten.")
