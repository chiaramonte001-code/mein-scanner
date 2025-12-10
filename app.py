import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Scanner Pro")

# --- LOGIN BEREICH ---
code = st.text_input("Passwort", type="password")

if code != "PRO-2025":
    st.error("Gesperrt. Code kaufen!")
    st.stop()

st.success("Scanner läuft!")

# --- START BUTTON ---
if st.button("Start"):
    # Daten laden
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Liste vorbereiten
        clean_data = []
        
        # Schleife durch die Daten
        for coin in 
            clean_data.append({
                "Name": coin['name'],
                "Preis": coin['current_price'],
                "Trend": coin['price_change_percentage_24h']
            })
            
        # Tabelle anzeigen
        st.dataframe(pd.DataFrame(clean_data))
        
    except Exception as e:
        st.error("Fehler beim Laden der Daten.")
        st.write(e)
