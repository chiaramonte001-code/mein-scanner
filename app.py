import streamlit as st
from PIL import Image
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from streamlit_drawable_canvas import st_canvas
from pdf2docx import Converter
import io
import os
import pdfplumber

st.set_page_config(page_title="Pro PDF Suite", page_icon="📝", layout="wide")

# --- LOGIN ---
with st.sidebar:
    st.title("🔒 Pro Suite")
    passwort = st.text_input("Lizenzschlüssel", type="password")
    if passwort != "PRO-2025":
        st.warning("Bitte einloggen.")
        st.markdown("👉 **[Zugang kaufen (5 CHF)](https://paypal.me/DEINNAME)**")
        st.stop()
    st.success("Premium Aktiv")

st.title("📝 Ultimate PDF Suite")

# Menü
menu = ["Bilder zu PDF", "PDF zu Word (Bearbeiten)", "PDF Unterschreiben", "PDF Zusammenfügen"]
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

# --- 2. PDF ZU WORD (NEU!) ---
elif choice == "PDF zu Word (Bearbeiten)":
    st.header("✏️ PDF in Word umwandeln")
    st.info("Der beste Weg, um Texte zu bearbeiten: Wandle das PDF in Word um, editiere es dort und speichere es neu.")
    
    pdf_file = st.file_uploader("PDF hochladen", type="pdf")
    
    if pdf_file and st.button("In Word Konvertieren"):
        with st.spinner("Starte KI-Konvertierung..."):
            # Temporäre Datei speichern (pdf2docx braucht eine echte Datei)
            with open("temp.pdf", "wb") as f:
                f.write(pdf_file.getbuffer())
            
            # Konvertieren
            cv = Converter("temp.pdf")
            cv.convert("temp.docx", start=0, end=None)
            cv.close()
            
            # Word Datei laden
            with open("temp.docx", "rb") as f:
                docx_data = f.read()
            
            # Aufräumen (Dateien löschen)
            os.remove("temp.pdf")
            os.remove("temp.docx")
            
            st.success("Erfolgreich umgewandelt!")
            st.download_button(
                label="⬇️ Word-Datei herunterladen (.docx)",
                data=docx_data,
                file_name="bearbeitbar.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# --- 3. PDF UNTERSCHREIBEN ---
elif choice == "PDF Unterschreiben":
    st.header("✍️ Dokument unterschreiben")
    source_file = st.file_uploader("PDF hochladen", type="pdf")
    st.write("Unterschrift zeichnen:")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)", stroke_width=2, stroke_color="#000000",
        background_color="#ffffff", height=150, width=400, drawing_mode="freedraw", key="canvas"
    )

    if source_file and canvas_result.image_data is not None and st.button("Stempeln"):
        with st.spinner("Verarbeite..."):
            # Signatur erstellen
            signature_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            img_byte_arr = io.BytesIO()
            signature_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            can.drawImage(img_byte_arr, 300, 50, width=150, height=80, mask='auto')
            can.save()
            packet.seek(0)
            
            # Mischen
            new_pdf = PdfReader(packet)
            existing_pdf = PdfReader(source_file)
            output = PdfWriter()
            
            for i in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[i]
                if i == len(existing_pdf.pages) - 1: # Nur letzte Seite
                    page.merge_page(new_pdf.pages[0])
                output.add_page(page)
            
            out_stream = io.BytesIO()
            output.write(out_stream)
            st.download_button("⬇️ Fertiges PDF", out_stream.getvalue(), "signed.pdf", "application/pdf")

# --- 4. MERGER ---
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

