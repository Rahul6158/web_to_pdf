import streamlit as st
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
import tempfile
import os

def scrape_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])  # Include headings
    images = soup.find_all('img')
    return content, images

def create_html(content, images):
    html_content = "<html><body>"
    for element in content:
        if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            html_content += f"<{element.name}>{element.text}</{element.name}>"
    for img in images:
        img_url = img['src']
        # Handle absolute and relative image URLs
        if not img_url.startswith('http'):
            img_url = requests.compat.urljoin(url, img_url)
        html_content += f"<img src='{img_url}' style='max-width:100%; height:auto;' />"
    html_content += "</body></html>"
    return html_content

def generate_pdf(html_content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        HTML(string=html_content).write_pdf(tmpfile.name)
        return tmpfile.name

# Streamlit app
st.title("Webpage to PDF Converter")

url = st.text_input("Enter the URL of the webpage:")

if st.button("Generate PDF"):
    if url:
        st.write("Processing...")
        content, images = scrape_webpage(url)
        html_content = create_html(content, images)
        pdf_file = generate_pdf(html_content)
        
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", data=f, file_name="output.pdf")
        
        os.remove(pdf_file)  # Clean up the temporary file
    else:
        st.error("Please enter a URL.")
