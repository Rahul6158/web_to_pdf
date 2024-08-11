import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image

def display_pdf(pdf_file):
    # Convert PDF to images
    images = convert_from_bytes(pdf_file.read())
    
    # Create a scrollable container
    with st.beta_expander("PDF Viewer", expanded=True):
        for img in images:
            st.image(img, use_column_width=True)

st.title("Scrollable PDF Viewer")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    display_pdf(uploaded_file)
