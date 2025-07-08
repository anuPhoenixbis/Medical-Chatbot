from src.helper import load_pdf, text_chunking, download_huggingfaceEmbeddings
from langchain_community.vectorstores import Chroma

extracted_data = load_pdf("data")
text_chunks = text_chunking(extracted_data)
embeddings = download_huggingfaceEmbeddings()

#setting up the Chroma vector store
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./nvidia_chroma_db"
)

batch_size = 500
for i in range(0, len(text_chunks), batch_size):
    batch = text_chunks[i : i + batch_size]
    vectorstore.add_documents(batch)

vectorstore.persist()
# vector_store = None  # Clear the variable to free up memory
print("Indexing completed and stored in 'chroma_db' directory.")