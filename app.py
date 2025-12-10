import streamlit as st
import requests
import pandas as pd
import time

# --- KONFIGURATION ---
# Falls die Public API spinnt, nutzen wir hier einen Fallback
API_URL = "https://api.coingecko.com/api/v3/coins/markets"

st.set_page_config(page_title="Crypto Pro", layout="wide")

# --- LOGIN ---
st.sidebar.title("🔒 Login")
pw = st.sidebar.text_input("Passwort", type="password")

if pw != "PRO-2025":
    st.warning("Bitte einloggen.")
    st.stop()

st.sidebar.success("Eingeloggt")

# --- HAUPT APP ---
st.title("🚀 Crypto Scanner Pro")

if st.button("Markt Scannen"):
    with st.spinner("Lade Daten..."):
        try:
            # Wir fragen die API ab
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 20,
                "page": 1,
                "sparkline": "false"
            }
            
            # Timeout wichtig, damit es nicht ewig hängt
            response = requests.get(API_URL, params=params, timeout=10)
            
            # Prüfen: War die Anfrage erfolgreich? (Code 200 = OK)
            if response.status_code == 200:
                data = response.json()
                
                # Prüfen: Haben wir überhaupt eine Liste bekommen?
                if isinstance(data, list) and len(data) > 0:
                    
                    # Wir bauen die Liste manuell auf (sicherer als direkt in Pandas)
                    clean_list = []
                    for coin in 
                        # .get() verhindert Absturz bei fehlenden Werten
                        name = coin.get('name', 'N/A')
                        price = coin.get('current_price', 0)
                        change = coin.get('price_change_percentage_24h', 0)
                        
                        # Signal berechnen
                        signal = "⚪ HALTEN"
                        if change is not None:
                            if change < -3: signal = "🟢 KAUFEN"
                            if change > 3: signal = "🔴 VERKAUFEN"
                        else:
                            change = 0 # Fallback
                            
                        clean_list.append({
                            "Coin": name,
                            "Preis ($)": price,
                            "Trend (24h)": f"{change:.2f} %",
                            "Signal": signal
                        })
                    
                    # Jetzt erst Tabelle machen
                    df = pd.DataFrame(clean_list)
                    
                    # Stylen und anzeigen
                    st.success(f"{len(df)} Coins erfolgreich geladen!")
                    st.dataframe(df, use_container_width=True)
                    
                else:
                    st.error("API hat keine Daten geschickt (Liste leer).")
                    st.json(data) # Zeigt uns, was stattdessen ankam
            
            elif response.status_code == 429:
                st.error("Zu viele Anfragen! (Rate Limit). Warte 1 Minute.")
            else:
                st.error(f"API Fehler Code: {response.status_code}")
                
        except Exception as e:
            st.error("Ein unerwarteter Fehler ist aufgetreten.")
            st.write(e)
