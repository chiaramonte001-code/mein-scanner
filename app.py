import streamlit as st

# --- HIER DEIN PASSWORT ÄNDERN ---
GEHEIM_CODE = "PRO-2025"
BEZAHL_LINK = "https://paypal.me/DEINNAME/5"
# ---------------------------------

st.title("🚀 Mein Krypto Scanner")

# 1. Die Abfrage
passwort = st.text_input("Bitte Zugangscode eingeben:", type="password")

if passwort != GEHEIM_CODE:
    # --- ZUSTAND: GESPERRT ---
    st.error("STOP! Dieses Tool ist nur für Mitglieder.")
    st.write("Sende mir 5 CHF, um den Zugangscode zu erhalten.")
    st.link_button("👉 Jetzt Code kaufen (PayPal)", BEZAHL_LINK)
    
else:
    # --- ZUSTAND: OFFEN (Dein Tool) ---
    st.success("✅ Zugang gewährt!")
    st.balloons()
    
    st.header("Analyse für Heute")
    col1, col2 = st.columns(2)
    col1.metric("Bitcoin Empfehlung", "KAUFEN", "Stark")
    col2.metric("Ziel-Preis", "98.500 $", "+2%")
    
    st.write("Hier steht deine exklusive Info für Kunden...")
