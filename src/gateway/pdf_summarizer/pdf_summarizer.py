"""
    PDF Summarizer

"""

# Python built-in module for handling temporary files.
import tempfile

# File Selector
from tkinter.filedialog import askopenfilename

# Core Langchain library
from langchain.llms import OpenAI

# PDF Loader and LangChain Output Parser
from langchain.document_loaders import PyPDFLoader

# Langchain Summarizer
from langchain.chains.summarize import load_summarize_chain

# Text Splitter
from langchain.text_splitter import CharacterTextSplitter

# Langchain library that represents a document.
from langchain.docstore.document import Document

# Output Parser
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser

# Pydantic BaseModel
from pydantic import BaseModel, Field

# Read Env variables
from dotenv import load_dotenv

load_dotenv()


class Summary(BaseModel):
    """ 
    doc string
    """
    summary: str = Field(description="Summary of the PDF")


def pdf_reader(file):
    """
        doc string
    """
    if file is not None:
        print(type(file))
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.file.read())
            pdf_path = tmp_file.name
            return pdf_path


def pdf_summarizer(doc: str):
    """
    doc string

    """
    llm = OpenAI(temperature=0.9)
    loader = PyPDFLoader(doc)
    pages = loader.load_and_split()
    combined_content = ''.join([p.page_content for p in pages])
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 800,
        chunk_overlap  = 200,
        length_function = len,
    )
    texts = text_splitter.split_text(combined_content)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    parser = PydanticOutputParser(pydantic_object=Summary)
    fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    summary = fix_parser.parse(summary)
    return summary

if __name__ == "__main__":
    FILENAME = askopenfilename()
    print(pdf_summarizer(FILENAME))