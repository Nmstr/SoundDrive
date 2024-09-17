from .songs import query as query_songs_in_db
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
from whoosh.writing import AsyncWriter
import threading
import os

class SearchEngine:
    #  TODO: Implement a popularity score system to rank more liked songs higher
    def __init__(self):
        self.index_dir_path = os.getenv('XDG_CACHE_HOME', default=os.path.expanduser('~/.cache')) + '/SoundDrive/SearchIndex'
        self.create_index()
        index_thread = threading.Thread(target=self.index_songs)
        index_thread.start()

    def create_index(self):
        # Define the schema
        schema = Schema(title=TEXT(stored=True),
                        artist=TEXT(stored=True),
                        id=NUMERIC(stored=True),
                        score=NUMERIC(stored=True))

        # Create the index
        if not os.path.exists(self.index_dir_path):
            os.mkdir(self.index_dir_path)
        create_in(self.index_dir_path, schema)

    def index_songs(self):
        index = open_dir(self.index_dir_path)

        # Add documents to the index
        writer = AsyncWriter(index)
        all_songs = query_songs_in_db()
        for song in all_songs:
            writer.add_document(title=song[1], artist=song[3], id=song[0], score=100)
        writer.commit()

    def query(self, query_text):
        index = open_dir(self.index_dir_path)

        with index.searcher() as searcher:
            # Define the query parser and parse the query
            parser = MultifieldParser(["title", "artist"], schema=index.schema)
            parser.add_plugin(FuzzyTermPlugin())

            modified_query_text = f"{query_text}~{2}"

            # Perform the search
            query_result = parser.parse(modified_query_text)
            results = searcher.search(query_result, limit=50)

            song_ids = []
            for result in results:
                song_ids.append(result["id"])
            return song_ids
