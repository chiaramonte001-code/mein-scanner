import streamlit as st
import requests
import time

# --- KONFIGURATION ---
GEHEIM_CODE = "PRO-2025"
BEZAHL_LINK = "https://paypal.me/DEINNAME/5"

st.set_page_config(page_title="Crypto Sniper", page_icon="📈")
st.title("📈 Crypto Sniper 2025")

# --- LOGIN ---
passwort = st.text_input("🔑 Zugangscode eingeben:", type="password")

if passwort != GEHEIM_CODE:
    st.info("🔒 Dieses Profi-Tool ist gesperrt.")
    st.write("Live-Daten nur für Mitglieder.")
    st.stop()

# --- HAUPT PROGRAMM ---
st.success("🔓 Zugang aktiv.")

if st.button("🔄 Markt Scannen"):
    with st.spinner("Analysiere Daten..."):
        try:
            # Wir nutzen eine stabilere URL
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
            res = requests.get(url, timeout=10)
            
            if res.status_code == 200:
                data = res.json()
                
                # Bitcoin Daten
                btc = data.get('bitcoin', {})
                btc_price = btc.get('usd', 0)
                btc_change = btc.get('usd_24h_change', 0)

                # Ethereum Daten
                eth = data.get('ethereum', {})
                eth_price = eth.get('usd', 0)
                eth_change = eth.get('usd_24h_change', 0)

                col1, col2 = st.columns(2)
                col1.metric("Bitcoin", f"{btc_price} $", f"{btc_change:.2f}%")
                col2.metric("Ethereum", f"{eth_price} $", f"{eth_change:.2f}%")
                
                # Signal
                if btc_change < -2:
                    st.success("KAUF-SIGNAL (Preis gefallen)")
                elif btc_change > 5:
                    st.error("VERKAUF-SIGNAL (Preis gestiegen)")
                else:
                    st.info("Markt Neutral")
                    
            else:
                st.error("API überlastet. Warte 10 Sekunden.")
                
        except Exception as e:
            st.error(f"Verbindungsfehler: {e}")
            st.warning("Versuche es gleich nochmal.")
