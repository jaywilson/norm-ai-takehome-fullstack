from pathlib import Path
from typing import List

from llama_index.core.schema import Document
from llama_cloud_services import LlamaParse
from llama_cloud_services.parse.utils import ResultType
from llama_index.core import SimpleDirectoryReader


project_root = Path(__file__).parent.parent


class LlamaParser:
    @classmethod
    async def parse(cls) -> List[Document]:
        """
        This parse method uses LlamaParse to parse the PDF document. It uses an LLM
        parser to identify document sections and returns the text of the document
        formatted as Markdown.

        The example document of course could be parsed with simple text parsing, but
        Llama parse would generalize better although at significantly increased cost.
        """

        parser = LlamaParse(result_type=ResultType.MD)
        file_extractor = {".pdf": parser}
        reader = SimpleDirectoryReader(
            input_files=[f"{project_root}/docs/laws.pdf"],
            file_extractor=file_extractor
        )
        documents = await reader.aload_data()

        law_documents = []
        section = None
        text = ''
        for doc in documents:
            for line in doc.text.split('\n'):
                if line.startswith('#'):
                    if section is not None and text != '':
                        law_documents.append(
                            Document(
                                text=text,
                                metadata={"Section": section}
                            )
                        )
                        text = ''
                    section = line[2:]
                else:
                    text += line

        return law_documents
