import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pdfkit
import tempfile

# Function to fetch and parse the webpage
def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        st.error(f"Failed to retrieve the webpage: {e}")
        return None

# Function to fetch external CSS files and include them in the HTML content
def include_css(soup, base_url):
    css_links = soup.find_all("link", rel="stylesheet")
    for link in css_links:
        href = link.get("href")
        if href:
            if not href.startswith("http"):
                href = requests.compat.urljoin(base_url, href)
            try:
                css_response = requests.get(href)
                css_response.raise_for_status()
                style_tag = soup.new_tag("style", type="text/css")
                style_tag.string = css_response.text
                link.replace_with(style_tag)
            except requests.RequestException as e:
                st.error(f"Failed to retrieve CSS file {href}: {e}")
    return str(soup)

# Function to extract the main content of the webpage
def extract_main_content(soup):
    main_content = soup.find('main') or soup.find('article')
    if not main_content:
        main_content = soup.find('div', class_='main-content') or soup.find('div', id='main-content') or soup.find('div', class_='content') or soup.find('div', id='content')
    if main_content:
        return str(main_content)
    else:
        st.warning("Main content not found, using full page content.")
        return str(soup)

# Function to modify the HTML to center-align images and add custom styles
def style_html_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    if not soup.html:
        html_tag = soup.new_tag("html")
        soup.insert(0, html_tag)
    if not soup.head:
        head_tag = soup.new_tag("head")
        soup.html.insert(0, head_tag)

    style_tag = soup.new_tag("style")
    style_tag.string = """
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
    }
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 70%;
        height: auto;
    }
    p {
        text-align: justify;
    }
    """
    soup.head.append(style_tag)

    return str(soup)

# Function to convert the HTML content to a PDF
def convert_html_to_pdf(html_content):
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as html_file:
        html_file.write(html_content.encode('utf-8'))
        html_file_path = html_file.name

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        pdf_file_path = pdf_file.name

    try:
        pdfkit.from_file(html_file_path, pdf_file_path)
        with open(pdf_file_path, "rb") as f:
            pdf_content = f.read()
        return pdf_content
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")
        return None
    finally:
        # Clean up temporary files
        os.remove(html_file_path)
        os.remove(pdf_file_path)

# Main Streamlit app
def main():
    st.title("Webpage to PDF Converter")

    num_links = st.number_input("Enter the number of links (1 to 6):", min_value=1, max_value=6, step=1)
    urls = []
    for i in range(num_links):
        url = st.text_input(f"Enter the URL for link {i + 1}:")

        if url:
            urls.append(url)

    if st.button("Generate PDF"):
        combined_html_content = ""

        for url in urls:
            html_content = fetch_webpage(url)
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                base_url = requests.compat.urljoin(url, '/')
                html_with_css = include_css(soup, base_url)

                main_content_html = extract_main_content(BeautifulSoup(html_with_css, "html.parser"))
                styled_html_content = style_html_content(main_content_html)

                combined_html_content += styled_html_content
            else:
                st.error(f"Failed to retrieve the webpage content for URL: {url}")

        if combined_html_content:
            # Convert the combined HTML to a PDF using pdfkit
            pdf_content = convert_html_to_pdf(combined_html_content)

            if pdf_content:
                # Provide the final PDF for download
                st.download_button(label="Download PDF", data=pdf_content, file_name="combined_webpage.pdf", mime="application/pdf")
        else:
            st.warning("No valid content to generate PDF.")

if __name__ == "__main__":
    main()
