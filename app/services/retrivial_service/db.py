from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class Retrieve:
    def __init__(self):
        self.embedding_function = HuggingFaceEmbeddings(
            model_name = " model_name=./ai-models/all-MiniLM-L6-v2"
        )
        self.vector_stores = Chroma(
            collection_name="cv_collection",
            embedding_function=self.embedding_function,
            persist_directory="../chromadb"
        )
    def get_db(self, docs):
        self.vector_stores.from_documents(docs)
        self.vector_stores.persist()
        return self.vector_stores



