from .songs import query as query_songs_in_db
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.writing import AsyncWriter
import os

class SearchEngine:
    def __init__(self):
        self.create_index()
        self.index_songs()

    def create_index(self):
        # Define the schema
        schema = Schema(title=TEXT(stored=True),
                        artist=TEXT(stored=True),
                        id=NUMERIC(stored=True),
                        score=NUMERIC(stored=True))

        # Create the index directory if it doesn't exist
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")

        # Create the index
        create_in("indexdir", schema)

    def index_songs(self):
        # Open the index
        ix = open_dir("indexdir")

        # Add documents to the index
        writer = AsyncWriter(ix)
        all_songs = query_songs_in_db()
        for song in all_songs:
            writer.add_document(title=song[1], artist=song[3], id=song[0], score=100)
        writer.commit()

    def query(self, query_text):
        # Open the index
        ix = open_dir("indexdir")
        # Create a searcher
        with ix.searcher() as searcher:
            # Define the query parser and parse the query
            parser = MultifieldParser(["title", "artist"], schema=ix.schema)
            parser.add_plugin(FuzzyTermPlugin())

            # Create a modified query text
            modified_query_text = f"{query_text}~{2}"

            # Search for the query
            query_result = parser.parse(modified_query_text)
            results = searcher.search(query_result, limit=50)

            # Print the results
            song_ids = []
            for result in results:
                song_ids.append(result["id"])
            return song_ids
