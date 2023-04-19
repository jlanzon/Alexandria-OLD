from flask import Flask, request, jsonify
from flask_cors import CORS
import requests 
import os
import hashlib

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

def compute_file_hash(file_path):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file provided."})
        
        file = request.files["file"]
        if not file.filename.endswith(".pdf"):
            return jsonify({"status": "error", "message": "Invalid file type. Please upload a PDF file."})

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        file_hash = compute_file_hash(file_path)
        existing_files = [f for f in os.listdir(UPLOAD_FOLDER) if compute_file_hash(os.path.join(UPLOAD_FOLDER, f)) == file_hash]
        if len(existing_files) > 1:
            os.remove(file_path)
            return jsonify({"status": "error", "message": "File already exists in the database."})
        else:
            text = scrape_pdf(file_path)
        temp_index_file_path = os.path.join(INDEX_FOLDER, f"{file.filename}.pdf")
        file_name = file.filename
        add_document_to_index(index, file_name, text, file_hash)

        # Can delete after use to save space
        # os.remove(temp_index_file_path)
        index_pdf(text, temp_index_file_path)
        return jsonify({"status": "success", "message": "File indexed."})
        
    except Exception as e:
        print(f"Error processing request: {e}")
        response = jsonify({"error": "Invalid request data"})
        return response

    try:
        if "url" in request.json:
            url = request.json["url"]
            if url.lower().endswith(".pdf"):
                response = requests.get(url)
                if response.status_code == 200:
                    file_name = url.split("/")[-1]
                    file_path = os.path.join(UPLOAD_FOLDER, file_name)
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    file_hash = compute_file_hash(file_path)
                    existing_files = [f for f in os.listdir(UPLOAD_FOLDER) if compute_file_hash(os.path.join(UPLOAD_FOLDER, f)) == file_hash]
                    if len(existing_files) > 1:
                        os.remove(file_path)
                        return jsonify({"status": "error", "message": "File already exists in the database."})
                    else:
                        text = scrape_pdf(file_path)
                    index_file_path = os.path.join(INDEX_FOLDER, f"{file_name}.pdf")
                    file_name = file.filename
                    add_document_to_index(index, file_name, text, file_hash)

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
        response = jsonify({"error": "Invalid request data"})
        return response


# Search
@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query')
    results = search(index, query)
    return jsonify(results)

if __name__ == "__main__":
    app.run()
