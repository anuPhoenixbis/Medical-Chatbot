from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings


#extract the text from a PDF file
def load_pdf(data):
    loader = DirectoryLoader(
        data,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
    )
    documents = loader.load()
    return documents

#text Chunking
def text_chunking(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

#download the embedding model from huggingface

def download_huggingfaceEmbeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings
