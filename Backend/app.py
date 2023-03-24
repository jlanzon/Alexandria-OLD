import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS library
import base64
import tempfile
from pdf_extractor import extract_text_from_pdf
from search_engine import add_document_to_index, search, index

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route('/upload', methods=['POST'])
def upload():
    pdf_file = request.files['file']
    file_path = tempfile.mktemp(suffix='.pdf')
    pdf_file.save(file_path)
    print("Here")
    text = extract_text_from_pdf(file_path)
    os.remove(file_path)
    add_document_to_index(index, pdf_file.filename, text)
    return jsonify({"status": "success", "message": "File indexed."})

@app.route('/search', methods=['GET'])
def search_api():
    query = request.args.get('query', '')
    results = search(index, query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
