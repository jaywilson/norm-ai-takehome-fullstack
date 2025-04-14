from utils import DocumentService, QdrantService, Output


class LawService:
    def __init__(self) -> None:
        self.doc_service = DocumentService()
        self.index = QdrantService()

    async def start(self) -> None:
        docs = await self.doc_service.create_documents()
        self.index.connect()
        self.index.load(docs)

    async def stop(self) -> None:
        self.index.stop()

    async def query(self, query: str, top_k: int) -> Output:
        return await self.index.query(query, top_k)