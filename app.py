import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Scanner")

# Login
code = st.text_input("Code", type="password")
if code != "PRO-2025":
    st.warning("Gesperrt.")
    st.stop()

st.success("Scanner bereit!")

if st.button("Starten"):
    # Daten laden
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd", 
        "order": "market_cap_desc", 
        "per_page": 20, 
        "page": 1
    }
    
    try:
        r = requests.get(url, params=params)
        data = r.json()
        
        # TRICK: Wir werfen die Daten direkt in die Tabelle (ohne Schleife!)
        df = pd.DataFrame(data)
        
        # Wir zeigen nur die wichtigen Spalten an
        simple_df = df[['name', 'current_price', 'price_change_percentage_24h', 'total_volume']]
        
        # Spalten umbenennen für schöne Optik
        simple_df.columns = ['Name', 'Preis ($)', 'Trend (24h %)', 'Volumen']
        
        st.subheader("Markt Daten")
        st.dataframe(simple_df)
        
    except Exception as e:
        st.error("Fehler.")
        st.write(e)
