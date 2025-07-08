from flask import Flask, request, jsonify, render_template
from src.helper import download_huggingfaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA , LLMChain
from langchain_community.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from src.prompt import *
import os
import subprocess

app = Flask(__name__)

"""
I want to check if the dir "./chroma_db" exists then we will just initialize 
the vectorstore here. Otherwise , we will run the store_index.py file and 
then initialize the vectorstore because now the embeddings will be ready to
be queried from
"""

#initialize the vector store
if not os.path.exists("./chroma_db"):
    print("[INFO] No existing ChromaDB found. Running store_index.py to create embeddings...")
    try:
        subprocess.run(["python", "store_index.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] store_index.py failed: {e}")
    # Run the script that generates and persists
else:
    print("[INFO] Existing ChromaDB found. Using the existing embeddings.")
    
# Load the vector store
embeddings = download_huggingfaceEmbeddings()
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

print("[INFO] Vectorstore initialized and ready to use.")

prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=TEMPLATE)
chain_type_kwargs={"prompt" : prompt}

# chain_type_kwargs = {
#     "prompt": prompt,
# }

llm = Ollama(
    model="llama2",
    temperature=0.7,
    top_p=0.9,
    repeat_penalty=1.1,
    num_predict=512  # Use this instead of max_tokens
)

# qa_chain = load_qa_chain(
#     llm=llm,           # Ollama-compatible model
#     chain_type="stuff",
#     prompt=prompt
# )

# qa = RetrievalQA(
#     retriever=retriever,
#     combine_documents_chain=qa_chain,
#     return_source_documents=True
# )

# from langchain_core.prompts import RunnablePromptTemplate


def prompt_wrapper(input_dict):
    return prompt.format(**input_dict)

# LCEL-style QA chain using Ollama
chain = (
    RunnableMap({"context": retriever, "question": lambda x: x["question"]})
    | prompt_wrapper
    | llm
    | StrOutputParser()
)


@app.route('/')
def home():
    return render_template('chat.html') # Render the chat interface when the root URL is accessed

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # result = qa(query)
    # answer = result["result"]
    answer = chain.invoke({"question": query})
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run(debug=True)