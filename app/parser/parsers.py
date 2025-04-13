from pathlib import Path
from typing import List

from llama_index.core.schema import Document
from llama_cloud_services import LlamaParse
from llama_cloud_services.parse.utils import ResultType
from llama_index.core import SimpleDirectoryReader


project_root = Path(__file__).parent.parent.parent


class LlamaParser:
    @classmethod
    def parse(cls) -> List[Document]:
        law_documents = []

        parser = LlamaParse(
            result_type=ResultType.MD
        )

        section = None
        text = ''
        file_extractor = {".pdf": parser}
        documents = SimpleDirectoryReader(input_files=[f"{project_root}/docs/laws.pdf"], file_extractor=file_extractor).load_data()
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
