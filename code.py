import streamlit as st
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from io import BytesIO

# Function to fetch and parse the webpage
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Failed to retrieve the webpage.")
        return None

# Function to fetch external CSS files and include them in the HTML content
def include_css(soup, base_url):
    css_links = soup.find_all("link", rel="stylesheet")
    for link in css_links:
        href = link.get("href")
        if href:
            if not href.startswith("http"):
                href = f"{base_url}/{href}"
            css_response = requests.get(href)
            if css_response.status_code == 200:
                style_tag = soup.new_tag("style", type="text/css")
                style_tag.string = css_response.text
                link.replace_with(style_tag)
    return str(soup)

# Function to extract the main content of the webpage
def extract_main_content(soup):
    # Adjust this part to fit the webpage structure
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
    
    # Ensure the <html> and <head> tags exist
    if not soup.html:
        html_tag = soup.new_tag("html")
        soup.insert(0, html_tag)
    if not soup.head:
        head_tag = soup.new_tag("head")
        soup.html.insert(0, head_tag)
    
    # Add custom styles
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
        width: 100%; /* Sets the image width to 100% of the container's width */
        height: auto; /* Maintains the aspect ratio of the image */
        margin-left: auto; /* Centers the image horizontally */
        margin-right: auto; /* Centers the image horizontally */
    }
    p {
        text-align: justify;
    }
    """
    soup.head.append(style_tag)
    
    return str(soup)

# Function to convert the HTML content to PDF and return as bytes
def convert_to_pdf(html_content):
    pdf = BytesIO()
    HTML(string=html_content).write_pdf(pdf)
    pdf.seek(0)
    return pdf

# Streamlit application
def main():
    st.title("Webpage to PDF Converter")
    
    url = st.text_input("Enter the URL of the webpage:")
    
    if st.button("Convert to PDF"):
        if url:
            html_content = fetch_webpage(url)
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                base_url = "/".join(url.split("/")[:-1])
                html_with_css = include_css(soup, base_url)
                
                # Extract main content
                main_content_html = extract_main_content(BeautifulSoup(html_with_css, "html.parser"))
                
                # Add custom styles
                styled_html_content = style_html_content(main_content_html)
                
                # Convert styled HTML to PDF
                pdf = convert_to_pdf(styled_html_content)
                
                st.success("PDF generated successfully!")
                st.download_button(
                    label="Download PDF",
                    data=pdf,
                    file_name="webpage.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Please enter a valid URL.")

if __name__ == "__main__":
    main()
