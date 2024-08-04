import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

# Function to remove selected pages from a PDF
def remove_pages(input_pdf, pages_to_remove):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        if page_num not in pages_to_remove:
            writer.add_page(reader.pages[page_num])

    return writer

# Function to shuffle pages in a PDF
def shuffle_pages(input_pdf, new_order):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page_num in new_order:
        writer.add_page(reader.pages[page_num])

    return writer

# Function to merge multiple PDFs
def merge_pdfs(pdf_list):
    merger = PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    return merger

# Streamlit app
def main():
    st.title("PDF Editor")
    
    menu = ["Remove Selected Pages", "Shuffle Pages", "Merge PDFs"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Remove Selected Pages":
        st.header("Remove Selected Pages")
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            num_pages = PdfReader(uploaded_file).get_num_pages()
            pages_to_remove = st.multiselect("Select pages to remove (0-indexed)", list(range(num_pages)))
            if st.button("Remove Pages"):
                output_writer = remove_pages(uploaded_file, pages_to_remove)
                output_path = "output_removed_pages.pdf"
                with open(output_path, "wb") as output_file:
                    output_writer.write(output_file)
                st.success(f"PDF saved without selected pages: {output_path}")
                with open(output_path, "rb") as file:
                    btn = st.download_button(label="Download PDF", data=file, file_name="output_removed_pages.pdf")

    elif choice == "Shuffle Pages":
        st.header("Shuffle Pages")
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
        if uploaded_file is not None:
            num_pages = PdfReader(uploaded_file).get_num_pages()
            new_order = st.text_input(f"Enter the new order of pages (comma separated, 0-{num_pages-1})")
            if st.button("Shuffle Pages"):
                new_order = [int(x) for x in new_order.split(",")]
                output_writer = shuffle_pages(uploaded_file, new_order)
                output_path = "output_shuffled_pages.pdf"
                with open(output_path, "wb") as output_file:
                    output_writer.write(output_file)
                st.success(f"PDF saved with shuffled pages: {output_path}")
                with open(output_path, "rb") as file:
                    btn = st.download_button(label="Download PDF", data=file, file_name="output_shuffled_pages.pdf")

    elif choice == "Merge PDFs":
        st.header("Merge PDFs")
        num_pdfs = st.number_input("Enter the number of PDFs to merge", min_value=2, max_value=10, step=1)
        uploaded_files = [st.file_uploader(f"Upload PDF {i+1}", type=["pdf"]) for i in range(num_pdfs)]
        
        if all(uploaded_files) and st.button("Merge PDFs"):
            merger = PdfMerger()
            for uploaded_file in uploaded_files:
                merger.append(uploaded_file)
            output_path = "output_merged.pdf"
            with open(output_path, "wb") as output_file:
                merger.write(output_file)
            st.success(f"Merged PDF saved as: {output_path}")
            with open(output_path, "rb") as file:
                btn = st.download_button(label="Download PDF", data=file, file_name="output_merged.pdf")

if __name__ == "__main__":
    main()
