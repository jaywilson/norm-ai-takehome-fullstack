from pathlib import Path
from typing import List

from PyPDF2 import PdfReader
from llama_index.core.schema import Document
from llmsherpa.readers import LayoutPDFReader


project_root = Path(__file__).parent.parent.parent


class SimpleParser:
    @classmethod
    def parse(cls) -> List[Document]:
        pdf_path = f"{project_root}/docs/laws.pdf"
        reader = PdfReader(pdf_path)
    
        sections: List[Document] = []
        cur_text = ''
        cur_section = None
        for page in reader.pages:
            text = page.extract_text()
            for word in text.splitlines():
                if cls.is_section_start(word):
                    if cur_section is not None:
                        sections.append(
                            Document(
                                metadata={"Section": cur_section},
                                text=cur_text,
                            ),
                        )
                    cur_section = word.strip()
                    cur_text = ''
                else:
                    cur_text += ' ' + word.strip()
    
        return sections
    
    @classmethod
    def is_section_start(cls, word: str) -> bool:
        parts = word.split('.')
        return len(parts) > 2


class LLMParser:
    pdf_path = f"{project_root}/docs/laws.pdf"
    llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"

    @classmethod
    def parse(cls) -> Document:
        pdf_reader = LayoutPDFReader(cls.llmsherpa_api_url)
        return pdf_reader.read_pdf(cls.pdf_path)

