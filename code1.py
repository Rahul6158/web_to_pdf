import streamlit as st
import fitz  # PyMuPDF

def view_pdf(pdf_file):
    # Open the PDF file
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    # Display each page of the PDF
    num_pages = pdf_document.page_count
    st.write(f"Number of pages: {num_pages}")

    for page_num in range(num_pages):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = pix.tobytes()
        st.image(img, caption=f"Page {page_num + 1}", use_column_width=True)

st.title("PDF Viewer")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    view_pdf(uploaded_file)
