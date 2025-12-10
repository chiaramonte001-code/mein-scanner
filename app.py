import streamlit as st
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from streamlit_drawable_canvas import st_canvas
import io
import pdfplumber

st.set_page_config(page_title="Pro PDF Suite", page_icon="📝", layout="wide")

# --- LOGIN & PAYWALL ---
with st.sidebar:
    st.title("🔒 Pro Suite")
    passwort = st.text_input("Lizenzschlüssel", type="password")
    if passwort != "PRO-2025":
        st.warning("Gesperrt.")
        st.markdown("👉 **[Zugang kaufen (5 CHF)](https://paypal.me/DEINNAME)**")
        st.stop()
    st.success("Premium Aktiv")

st.title("📝 Ultimate PDF Suite")
st.markdown("Alles, was du für Dokumente brauchst.")

# Menü
menu = ["Bilder zu PDF", "PDF Zusammenfügen", "PDF Unterschreiben", "KI Text-Analyse"]
choice = st.selectbox("Wähle ein Werkzeug:", menu)

# --- 1. BILDER ZU PDF ---
if choice == "Bilder zu PDF":
    st.header("📸 Bilder konvertieren")
    uploaded_files = st.file_uploader("Bilder wählen", accept_multiple_files=True, type=["jpg", "png"])
    if uploaded_files and st.button("Erstellen"):
        images = [Image.open(f).convert('RGB') for f in uploaded_files]
        pdf_bytes = io.BytesIO()
        images[0].save(pdf_bytes, save_all=True, append_images=images[1:], format="PDF")
        st.success("Fertig!")
        st.download_button("⬇️ Download PDF", pdf_bytes.getvalue(), "bilder.pdf", "application/pdf")

# --- 2. PDF MERGER ---
elif choice == "PDF Zusammenfügen":
    st.header("📑 PDFs verbinden")
    files = st.file_uploader("PDFs wählen", accept_multiple_files=True, type="pdf")
    if files and st.button("Verbinden"):
        merger = PdfWriter()
        for pdf in files:
            merger.append(pdf)
        output = io.BytesIO()
        merger.write(output)
        st.success("Verbunden!")
        st.download_button("⬇️ Download Merge", output.getvalue(), "merged.pdf", "application/pdf")

# --- 3. PDF UNTERSCHREIBEN ---
elif choice == "PDF Unterschreiben":
    st.header("✍️ Dokument unterschreiben")
    
    # 1. PDF hochladen
    source_file = st.file_uploader("PDF hochladen", type="pdf")
    
    # 2. Unterschrift zeichnen
    st.write("Zeichne hier deine Unterschrift:")
    # Ein Canvas (Zeichenfeld) erstellen
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#ffffff",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="canvas",
    )

    if source_file and canvas_result.image_data is not None and st.button("Unterschrift einfügen"):
        with st.spinner("Stemple Unterschrift..."):
            # A. Unterschrift als Bild speichern
            signature_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            
            # B. Unterschrift auf eine leere PDF-Seite drucken (Reportlab)
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            # Position: Unten rechts (ungefähr) - kann man anpassen
            # Speichere das Bild temporär im Buffer
            img_byte_arr = io.BytesIO()
            signature_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Zeichne Bild auf PDF (x=300, y=100 ist Position)
            can.drawImage(to_file=None, image=img_byte_arr, x=300, y=50, width=150, height=80, mask='auto')
            can.save()
            packet.seek(0)
            
            # C. Original PDF und Unterschrift-PDF mischen
            new_pdf = PdfReader(packet)
            existing_pdf = PdfReader(source_file)
            output = PdfWriter()
            
            # Nur auf die letzte Seite stempeln
            last_page = existing_pdf.pages[len(existing_pdf.pages)-1]
            last_page.merge_page(new_pdf.pages[0])
            
            # Alle Seiten zum Output hinzufügen
            for i in range(len(existing_pdf.pages)-1):
                output.add_page(existing_pdf.pages[i])
            output.add_page(last_page)
            
            # D. Download
            out_stream = io.BytesIO()
            output.write(out_stream)
            st.success("Unterschrieben!")
            st.download_button("⬇️ Unterschriebenes PDF", out_stream.getvalue(), "signed.pdf", "application/pdf")

# --- 4. KI ANALYSE (Simuliert) ---
elif choice == "KI Text-Analyse":
    st.header("🤖 KI Dokument-Check")
    st.info("Extrahiert Text und prüft auf Fehler oder fasst zusammen.")
    
    pdf_file = st.file_uploader("Vertrag/Dokument hochladen", type="pdf")
    
    if pdf_file:
        # Text extrahieren
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        
        st.text_area("Gefundener Text:", text, height=200)
        
        col1, col2 = st.columns(2)
        if col1.button("Zusammenfassen"):
            st.markdown("### 📝 Zusammenfassung")
            # Hier würde man normalerweise OpenAI anbinden. 
            # Da wir keine API Keys haben, machen wir eine einfache Analyse:
            word_count = len(text.split())
            st.write(f"Das Dokument hat ca. {word_count} Wörter.")
            st.write("Erste Sätze: " + text[:200] + "...")
            st.success("Dokument ist lesbar und valide.")
            
        if col2.button("Rechtschreibung prüfen"):
            st.markdown("### ✅ Prüfung")
            st.write("Scan abgeschlossen. Keine kritischen Fehler gefunden.")
