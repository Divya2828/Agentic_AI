import os
from typing import List
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
from dotenv import load_dotenv
from prompt import QA_Prompt

load_dotenv()


def build_vectorstore(pdf_path: str) -> FAISS:
    """Load PDF, split into chunks, create a FAISS vectorstore."""
    # Load PDF using pypdf
    reader = PdfReader(pdf_path)
    text = ""
    page_map = {}
    current_pos = 0
    
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        text += page_text + "\n"
        page_map[(current_pos, current_pos + len(page_text))] = page_num
        current_pos += len(page_text) + 1

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text)
    
    # Create metadata for chunks
    chunk_docs = []
    for i, chunk in enumerate(chunks):
        # Simple page tracking: estimate page from chunk index
        page_num = min(i // 5, len(reader.pages) - 1)  # Rough estimate
        chunk_docs.append({
            "page_content": chunk,
            "metadata": {"page": page_num, "chunk": i}
        })

    # Create embeddings and vectorstore
    embeddings = OpenAIEmbeddings(
        model=os.environ.get("EMBEDDING_MODEL"),
        openai_api_base=os.environ.get("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
        openai_api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Build vectorstore
    texts = [doc["page_content"] for doc in chunk_docs]
    metadatas = [doc["metadata"] for doc in chunk_docs]
    vectordb = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    
    return vectordb


def answer_question(vectordb: FAISS, question: str, conversation_history: List[dict] = None) -> str:
    """Answer a question using the vectorstore and OpenAI API directly with conversation history."""
    
    if conversation_history is None:
        conversation_history = []
    
    # Retrieve top-k relevant chunks
    docs = vectordb.similarity_search(question, k=4)
    
    if not docs:
        return "No relevant context found in the uploaded document."

    # Format context with page citations
    context = ""
    pages_cited = set()
    for doc in docs:
        page = doc.metadata.get("page", 0)
        pages_cited.add(page + 1)  # Convert to 1-based
        context += f"[Page {page + 1}]\n{doc.page_content}\n\n"

    # Call OpenAI API directly using OpenRouter
    client = OpenAI(
        base_url=os.environ.get("OPENAI_API_BASE", "https://openrouter.ai/api/v1"),
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    # Build messages: system prompt + conversation history + current question with context
    messages = [
        {
            "role": "system",
            "content": (QA_Prompt + "\n\nYou are in a continuous conversation. Remember previous exchanges.")
        }
    ]
    
    # Add conversation history (keep last 4 exchanges to manage token limits)
    messages.extend(conversation_history[-8:])  # Last 4 Q&A pairs
    
    # Add current question with context
    messages.append({
        "role": "user",
        "content": f"Context:\n\n{context}\n\nQuestion: {question}\n\nPlease answer using only the context above and cite the page numbers."
    })

    completion = client.chat.completions.create(
        model=os.environ.get("CHAT_MODEL"),
        messages=messages,
        temperature=0
    )

    answer = completion.choices[0].message.content
    return answer