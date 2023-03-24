# PDF Search Engine
A simple PDF search engine built using Python, Flask, Whoosh, and Next.js. This project allows users to upload PDF files, index their content, and search through them using a web interface.

# Features
Extract text from PDF files using PyPDF2
Index and search PDF content with Whoosh
Flask REST API for file uploads and searching
Next.js front-end for interacting with the API

# Installation
* Prerequisites
* Python 3.7+
* Node.js 12+

# Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/jlanzon/alexandria.git
cd pdf-search-engine
```

# Set Up the Back-end
Start the App:

```bash
cd backend
app.py
```
Install the required Python packages:
<!-- Not complete yet! -->
```bash
pip install -r requirements.txt
```
Run the Flask API:

```bash
python app.py
The Flask API will be available at http://localhost:5000.
```

Set Up the Front-end
Navigate to the pdf-search-frontend directory:

```bash
cd pdf-search-frontend
```
Install the required Node.js packages:

```typescript
npm install
```
Run the Next.js development server:

```bash
npm run dev
```

The front-end application will be available at http://localhost:3000.

## Usage
Open the front-end application in your web browser at http://localhost:3000.
Upload a PDF file using the file input field.
Search for content within the indexed PDF files using the search input field.
View the search results in the results section.
