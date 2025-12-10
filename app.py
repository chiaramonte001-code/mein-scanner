import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Scanner Pro")

# Login
code = st.text_input("Passwort", type="password")
if code != "PRO-2025":
    st.error("Gesperrt. Code kaufen!")
    st.stop()

# App
st.success("Scanner läuft!")

if st.button("Start"):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
    data = requests.get(url).json()
    
    clean_data = []
    for coin in 
        clean_data.append({
            "Name": coin['name'],
            "Preis": coin['current_price'],
            "Trend": coin['price_change_percentage_24h']
        })
        
    st.dataframe(pd.DataFrame(clean_data))
