import streamlit as st
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML

# Function to fetch and parse the webpage
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        st.error("Failed to retrieve the webpage.")
        return None

# Function to convert the webpage to PDF
def convert_to_pdf(html_content):
    html = HTML(string=html_content)
    pdf_path = 'webpage.pdf'
    html.write_pdf(pdf_path)
    return pdf_path

# Streamlit app
st.title("Webpage to PDF Converter")

url = st.text_input("Enter the URL of the webpage")

if st.button("Generate PDF"):
    if url:
        soup = fetch_webpage(url)
        if soup:
            # Extract content and format it as needed
            content = str(soup)
            
            # Convert HTML to PDF
            pdf_path = convert_to_pdf(content)
            
            # Provide download link
            st.success("PDF generated successfully!")
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name='webpage.pdf',
                    mime='application/pdf'
                )
    else:
        st.error("Please enter a URL.")
