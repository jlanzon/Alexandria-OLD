from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

# Replace these imports with the actual file names in your project
from pdf_extractor import extract_text_from_pdf
from search_engine import search, add_document_to_index, create_index, index
from pdf_scraper import download_pdf_from_url, scrape_pdf
from pdf_indexer import index_pdf


app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

UPLOAD_FOLDER = "uploaded_files"
INDEX_FOLDER = "index_files"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(INDEX_FOLDER):
    os.makedirs(INDEX_FOLDER)

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" in request.files:
            file = request.files["file"]
            if file.filename.endswith(".pdf"):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                text = scrape_pdf(file_path)
                temp_index_file_path = os.path.join(INDEX_FOLDER, f"{file.filename}.pdf")
                add_document_to_index(index,file.filename, text)
                # Can delete after use to save space
                # os.remove(temp_index_file_path)
                index_pdf(text, temp_index_file_path)
                return jsonify({"status": "success", "message": "File indexed."})
            else:
                return jsonify({"status": "error", "message": "Invalid file type. Please upload a PDF file."})
        elif "url" in request.json:
            url = request.json["url"]
            if url.lower().endswith(".pdf"):
                response = requests.get(url)
                if response.status_code == 200:
                    file_name = url.split("/")[-1]
                    file_path = os.path.join(UPLOAD_FOLDER, file_name)
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    text = scrape_pdf(file_path)
                    index_file_path = os.path.join(INDEX_FOLDER, f"{file_name}.pdf")
                    add_document_to_index(index,file.filename, text)
                    # Can delete after use to save space
                    # os.remove(temp_index_file_path)
                    index_pdf(text, index_file_path)
                    return jsonify({"status": "success", "message": "File indexed."})
                
                else:
                    return jsonify({"status": "error", "message": "Failed to download the file from the provided URL."})
            else:
                return jsonify({"status": "error", "message": "Invalid URL. Please provide a direct link to a PDF file."})
        else:
            return jsonify({"status": "error", "message": "No file or URL provided."})
        
    except Exception as e:
        print(f"Error processing request: {e}")
        print(f"Request data: {request.data}")
        print(f"Request files: {request.files}")
        print(f"Request JSON: {request.json}")
        response = jsonify({"error": "Invalid request data"})

# Search
@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query', '')
    results = search(index, query)
    print(results)
    return jsonify(results)


if __name__ == "__main__":
    app.run()
