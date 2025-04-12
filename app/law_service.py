from utils import DocumentService, QdrantService, Output


class LawService:
    def __init__(self) -> None:
        self.doc_service = DocumentService()
        self.index = QdrantService()

    def start(self) -> None:
        docs = self.doc_service.create_documents()
        self.index.connect()
        self.index.load(docs)

    def stop(self) -> None:
        self.index.stop()

    def query(self, query: str) -> Output:
        return self.index.query(query)