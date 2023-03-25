# pdf_scraper.py

import PyPDF2
import io
import requests

def download_pdf_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        return None

def scrape_pdf(file_path_or_url):
    text = ""
    pdf_file = None

    if file_path_or_url.startswith("http://") or file_path_or_url.startswith("https://"):
        pdf_file = download_pdf_from_url(file_path_or_url)
    else:
        pdf_file = open(file_path_or_url, "rb")

    if pdf_file:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {e}")
        finally:
            pdf_file.close()

    return text
