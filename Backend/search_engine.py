import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

def create_index(index_dir, schema):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    return create_in(index_dir, schema)

def add_document_to_index(index, doc_id, content):
    writer = index.writer()
    writer.add_document(id=doc_id, content=content)
    writer.commit()

def search(index, query_str, top_n=10):
    parser = QueryParser("content", index.schema)
    query = parser.parse(query_str)
    with index.searcher() as searcher:
        results = searcher.search(query, limit=top_n)
        return [(r['id'], r.score) for r in results]

schema = Schema(id=ID(unique=True, stored=True), content=TEXT)
index = create_index("index_dir", schema)
