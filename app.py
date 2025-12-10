import streamlit as st
from PIL import Image
from PyPDF2 import PdfMerger
import io

st.set_page_config(page_title="Pro PDF Tools", page_icon="📄")

# --- 1. LOGIN & PAYWALL ---
st.sidebar.header("🔒 Premium Zugang")
passwort = st.sidebar.text_input("Lizenzschlüssel eingeben", type="password")

if passwort != "PRO-2025":
    st.title("📄 Pro PDF Tools")
    st.warning("🔒 Dieses Tool ist geschützt.")
    st.markdown("""
    ### Warum Pro Tools?
    - 🚀 **Keine Werbung**
    - 🔒 **100% Sicher** (Daten bleiben privat)
    - ⚡ **Blitzschnell** (Bilder -> PDF, PDF Merge)
    
    👉 **[Lizenzschlüssel für 5 CHF kaufen](https://www.paypal.com/paypalme/DEINNAME/5CHF)**
    """)
    st.stop()

# --- 2. DIE APP (Nur für Zahler sichtbar) ---
st.sidebar.success("✅ Lizenz Aktiv")
st.title("🛠️ Dein PDF Werkzeugkasten")

option = st.selectbox("Was möchtest du tun?", 
                      ["Bilder zu PDF konvertieren", "PDFs zusammenfügen (Merger)"])

# --- MODUL A: BILDER ZU PDF ---
if option == "Bilder zu PDF konvertieren":
    st.subheader("📸 Bilder in 1 PDF umwandeln")
    uploaded_files = st.file_uploader("Lade Bilder hoch (JPG, PNG)", 
                                      accept_multiple_files=True, type=["jpg", "jpeg", "png"])
    
    if uploaded_files:
        if st.button("PDF Erstellen"):
            with st.spinner("Erstelle PDF..."):
                # Logik: Bilder öffnen und konvertieren
                image_list = []
                first_image = None
                
                for file in uploaded_files:
                    img = Image.open(file)
                    img = img.convert('RGB') # Wichtig für PDF Kompatibilität
                    if first_image is None:
                        first_image = img
                    else:
                        image_list.append(img)
                
                # Speichern im Arbeitsspeicher (RAM)
                pdf_buffer = io.BytesIO()
                if first_image:
                    first_image.save(pdf_buffer, save_all=True, append_images=image_list, format="PDF")
                    
                    st.success("Fertig! Dein PDF ist bereit.")
                    st.download_button(
                        label="⬇️ PDF Herunterladen",
                        data=pdf_buffer.getvalue(),
                        file_name="meine_bilder.pdf",
                        mime="application/pdf"
                    )

# --- MODUL B: PDF MERGER ---
elif option == "PDFs zusammenfügen (Merger)":
    st.subheader("📑 Mehrere PDFs verbinden")
    uploaded_pdfs = st.file_uploader("Lade PDFs hoch", 
                                     accept_multiple_files=True, type="pdf")
    
    if uploaded_pdfs:
        st.write(f"{len(uploaded_pdfs)} Dateien geladen.")
        
        if st.button("Zusammenfügen"):
            with st.spinner("Verbinde Dateien..."):
                merger = PdfMerger()
                output_buffer = io.BytesIO()
                
                for pdf in uploaded_pdfs:
                    merger.append(pdf)
                
                merger.write(output_buffer)
                merger.close()
                
                st.success("Erfolgreich verbunden!")
                st.download_button(
                    label="⬇️ Verbundenes PDF laden",
                    data=output_buffer.getvalue(),
                    file_name="komplett.pdf",
                    mime="application/pdf"
                )
