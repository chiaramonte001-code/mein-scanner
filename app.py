import streamlit as st
import requests
import time

# --- KONFIGURATION ---
GEHEIM_CODE = "PRO-2025"
BEZAHL_LINK = "https://paypal.me/DEINNAME/5"

st.set_page_config(page_title="Crypto Sniper", page_icon="📈")
st.title("📈 Crypto Sniper 2025")

# --- LOGIN BEREICH ---
passwort = st.text_input("🔑 Zugangscode eingeben:", type="password")

if passwort != GEHEIM_CODE:
    st.info("🔒 Dieses Profi-Tool ist gesperrt.")
    st.markdown(f"""
    **Was du bekommst:**
    - Live Bitcoin & Ethereum Preise
    - Automatische Kauf/Verkauf Signale
    - 24/7 Markt-Analyse
    
    [👉 Zugang jetzt freischalten (5 CHF)]({BEZAHL_LINK})
    """)
    st.stop() # HIER STOPPT DAS PROGRAMM FÜR NICHT-ZAHLER

# --- AB HIER NUR FÜR ZAHLENDE KUNDEN ---
st.success("🔓 Zugang aktiv. Markt wird analysiert...")

# Echte Daten holen (CoinGecko API - kostenlos)
def get_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    return requests.get(url).json()

# Button zum Aktualisieren
if st.button("🔄 Markt Scannen"):
    with st.spinner("Analysiere Charts..."):
        time.sleep(1) # Kurze Pause für Effekt
        data = get_data()
        
        btc_price = data['bitcoin']['usd']
        btc_change = data['bitcoin']['usd_24h_change']
        
        eth_price = data['ethereum']['usd']
        eth_change = data['ethereum']['usd_24h_change']

        # Darstellung in Spalten
        col1, col2 = st.columns(2)
        
        col1.metric("Bitcoin (BTC)", f"{btc_price} $", f"{btc_change:.2f}%")
        col2.metric("Ethereum (ETH)", f"{eth_price} $", f"{eth_change:.2f}%")
        
        # Einfache Strategie-Logik
        st.subheader("🤖 KI-Empfehlung:")
        if btc_change < -2:
            st.success("🟢 KAUF-SIGNAL! (Preis ist stark gefallen - 'Buy the dip')")
        elif btc_change > 5:
            st.error("🔴 VERKAUF-SIGNAL! (Gewinne mitnehmen)")
        else:
            st.warning("⚪ HALTEN (Markt ist neutral)")

st.write("---")
st.caption("Live-Daten via CoinGecko API")
