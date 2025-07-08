from src.helper import load_pdf, text_chunking, download_huggingfaceEmbeddings
from langchain_community.vectorstores import Chroma

extracted_data = load_pdf("data")
text_chunks = text_chunking(extracted_data)
embeddings = download_huggingfaceEmbeddings()

#setting up the Chroma vector store
vector_store = Chroma.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

vector_store.persist()
# vector_store = None  # Clear the variable to free up memory
print("Indexing completed and stored in 'chroma_db' directory.")