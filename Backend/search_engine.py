import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from whoosh.writing import BufferedWriter

schema = Schema(id=ID(unique=True, stored=True), content=TEXT(analyzer=StemmingAnalyzer()))

def create_index(index_dir, schema):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return create_in(index_dir, schema)
    else:
        return open_dir(index_dir)

def add_document_to_index(index, file_name, text, file_hash):
    with index.writer() as writer:
        writer.add_document(id=doc_id, content=content)

_searcher = None

def search(index, query_str, top_n=10):
    global _searcher

    if _searcher is None:
        _searcher = index.searcher()
    else:
        _searcher = index.searcher().refresh()

    parser = QueryParser("content", index.schema)
    query = parser.parse(query_str)

    results = _searcher.search(query, limit=top_n)
    return [(r['id'], r.score) for r in results]


index = create_index("index_dir", schema)
