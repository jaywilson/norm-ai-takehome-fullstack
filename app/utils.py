from typing import Sequence, Optional
import asyncio

from pydantic import BaseModel
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import BaseNode
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.core.query_engine import CitationQueryEngine
from dataclasses import dataclass
import os

from parser.parsers import LlamaParser

key = os.environ['OPENAI_API_KEY']

@dataclass
class Input:
    query: str
    file_path: str

@dataclass
class Citation:
    source: str
    text: str

class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]

class DocumentService:
    """
    Update this service to load the pdf and extract its contents.
    The example code below will help with the data structured required
    when using the QdrantService.load() method below. Note: for this
    exercise, ignore the subtle difference between llama-index's 
    Document and Node classes (i.e, treat them as interchangeable).

    docs = [
        Document(
            metadata={"Section": "Law 1"},
            text="Theft is punishable by hanging",
        ),
        Document(
            metadata={"Section": "Law 2"},
            text="Tax evasion is punishable by banishment.",
        ),
    ]
    """

    @staticmethod
    async def create_documents() -> Sequence[BaseNode]:
        return await LlamaParser.parse()

class QdrantService:
    def __init__(self):
        self.index: Optional[VectorStoreIndex] = None
    
    def connect(self) -> None:
        # todo use Qdrant async client
        # when I tried, insert_nodes fails
        client = QdrantClient(location=":memory:")
        vstore = QdrantVectorStore(client=client, collection_name='temp')

        Settings.embed_model=OpenAIEmbedding()
        Settings.llm=OpenAI(api_key=key, model="gpt-4")
        # picks up values from Settings
        self.index = VectorStoreIndex.from_vector_store(vector_store=vstore)

    def load(self, docs: Sequence[BaseNode]):
        # todo how to insert with async client
        # when using the async client this fails because _client is None
        # even if use_async is specified when creating the vector store
        # further debugging needed...
        self.index.insert_nodes(docs)
    
    async def query(self, query_str: str, top_k: int) -> Output:
        """
        This method needs to initialize the query engine, run the query, and return
        the result as a pydantic Output class. This is what will be returned as
        JSON via the FastAPI endpoint. Fee free to do this however you'd like, but
        it's worth noting that the llama-index package has a CitationQueryEngine...

        Also, be sure to make use of self.k (the number of vectors to return based
        on semantic similarity).

        # Example output object
        citations = [
            Citation(source="Law 1", text="Theft is punishable by hanging"),
            Citation(source="Law 2", text="Tax evasion is punishable by banishment."),
        ]

        output = Output(
            query=query_str,
            response=response_text,
            citations=citations
            )

        return output

        """

        # queries the embeddings for relevant sources and provides them
        # in the prompt to the LLM. Top K controls the number of sources
        # to include in the prompt (generally 2 to 3 seems to work well).

        # initializing the query engine here allows experimenting with top k
        # with every query, but depending on the cost of initializing it might
        # be preferable to initialize once on service startup with a fixed top k
        query_engine = CitationQueryEngine.from_args(
            index=self.index,
            similarity_top_k=top_k,
        )

        # todo using an an async query would allow the
        # python web server to perform better on a single thread
        response = query_engine.query(query_str)
        response_text = response.response

        citations = []
        for source in response.source_nodes:
            citations.append(Citation(source=source.metadata["Section"], text=source.text))

        output = Output(
            query=query_str,
            response=response_text,
            citations=citations
        )
        return output

    def stop(self):
        # placeholder to clean up any resources on shutdown
        return
       

async def main():
    # Example workflow
    doc_service = DocumentService() # implemented
    docs = await doc_service.create_documents() # implemented!

    index = QdrantService() # implemented
    index.connect() # implemented
    index.load(docs) # implemented

    output = await index.query("what happens if I steal?", 3) # implemented!
    print(f"OUTPUT: {output}")


if __name__ == "__main__":
    asyncio.run(main())





