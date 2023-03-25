import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from whoosh.writing import BufferedWriter
import pymongo
from dotenv import load_dotenv
import hashlib
# Mongo DB add
load_dotenv()
password = os.environ.get("herokupsw")
client = pymongo.MongoClient("mongodb+srv://jlanzon:"+ password + "@alexandria.j2vxudk.mongodb.net/?retryWrites=true&w=majority")
db = client["alexandria"]
collection = db["index_files"]
schema = Schema(id=ID(unique=True, stored=True), content=TEXT(analyzer=StemmingAnalyzer()))


def create_index(index_dir, schema):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    return create_in(index_dir, schema)

def add_document_to_index(index, writer, doc_id, content, file_hash=None):
    writer.add_document(id=doc_id, content=content)
    # This section will upload the indexed files to the cloud, as well as the local machine
    data = {"id": doc_id, "content": str(content), "file_hash": file_hash}
    collection.insert_one(data)
    
def create_temp_index_from_mongodb():
    temp_index_dir = "temp_index_dir"
    if not os.path.exists(temp_index_dir):
        os.mkdir(temp_index_dir)
    temp_index = create_index(temp_index_dir, schema)
    for doc in collection.find():
        add_document_to_index(temp_index, doc["id"], doc["content"])
    return temp_index




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




_searcher = None

def search(query_str, top_n=10):
    global _searcher
    temp_index = create_temp_index_from_mongodb()

    if _searcher is None:
        _searcher = temp_index.searcher()
    else:
        _searcher = temp_index.searcher().refresh(_searcher)

    parser = QueryParser("content", temp_index.schema)
    query = parser.parse(query_str)

    with temp_index.writer() as writer:
        results = _searcher.search(query, limit=top_n)
        return [(r['id'], r.score) for r in results]


index = create_index("/Backend/index_dir", schema)
writer = index.writer()


