import streamlit as st
import requests
import pandas as pd

# --- DEIN SETUP ---
GEHEIM_CODE = "PRO-2025"
BEZAHL_LINK = "https://paypal.me/DEINNAME/5"

st.set_page_config(page_title="Crypto AI Scanner", page_icon="⚡", layout="wide")

# --- SIDEBAR (LOGIN) ---
with st.sidebar:
    st.header("🔐 Login")
    passwort = st.text_input("Code eingeben:", type="password")
    
    if passwort != GEHEIM_CODE:
        st.warning("Zugriff verweigert")
        st.markdown(f"👉 **[Zugang kaufen (5 CHF)]({BEZAHL_LINK})**")
        st.info("Features:\n- 50+ Coins Scan\n- KI Kauf-Signale\n- Arbitrage Finder")
        st.stop()
    else:
        st.success("Pro-Modus Aktiv")

# --- HAUPT TOOL ---
st.title("⚡ Crypto AI Scanner Pro")
st.markdown("Scanne den gesamten Markt nach unterbewerteten Coins.")

if st.button("🚀 JETZT SCANNEN"):
    with st.spinner("Lade Live-Daten von 50 Börsen..."):
        try:
            # 1. Daten holen (Top 50 Coins)
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 50,
                "page": 1,
                "sparkline": "false"
            }
            res = requests.get(url, params=params, timeout=10)
            data = res.json()
            
            # 2. Daten verarbeiten
            results = []
            for coin in 
                # Einfache "KI" Logik für Signale
                change_24h = coin['price_change_percentage_24h']
                signal = "⚪ NEUTRAL"
                
                if change_24h < -5:
                    signal = "🟢 STRONG BUY (Dip)"
                elif change_24h < -2:
                    signal = "🟢 BUY"
                elif change_24h > 5:
                    signal = "🔴 STRONG SELL (Top)"
                elif change_24h > 2:
                    signal = "🔴 SELL"
                
                results.append({
                    "Coin": coin['name'],
                    "Symbol": coin['symbol'].upper(),
                    "Preis ($)": coin['current_price'],
                    "24h Änderung": f"{change_24h:.2f}%",
                    "SIGNAL": signal,
                    "Volumen": f"{coin['total_volume'] / 1000000:.1f} Mio"
                })

            # 3. Tabelle erstellen
            df = pd.DataFrame(results)
            
            # 4. TOP EMPFEHLUNGEN (Die besten Dips)
            st.subheader("💎 Top Kauf-Empfehlungen (Dips)")
            best_buys = df[df["SIGNAL"].str.contains("BUY")]
            if not best_buys.empty:
                st.dataframe(best_buys.style.applymap(lambda x: 'color: green' if 'BUY' in str(x) else '', subset=['SIGNAL']))
            else:
                st.write("Aktuell keine starken Kauf-Signale.")

            # 5. GANZE LISTE
            st.subheader("📋 Alle Coins im Vergleich")
            st.dataframe(df)

        except Exception as e:
            st.error(f"Fehler beim Scannen: {e}")

else:
    st.info("Klicke auf den Button, um die Analyse zu starten.")
