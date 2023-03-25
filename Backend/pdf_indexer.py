# pdf_indexer.py

def index_pdf(text, index_file_path):
    with open(index_file_path, "w", encoding="utf-8") as f:
        f.write(text)
