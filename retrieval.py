from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from groq import Groq
import streamlit as st
import os
from system_prompt import system_prompt
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_vectorstore():
    """Create vector store connection only when needed"""

    # ✅ Embedding model from HuggingFace
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    qdrant_client = QdrantClient(url="http://localhost:6333", port=6333)

    try:
        collection_info = qdrant_client.get_collection("health_report")
        if collection_info:
            return QdrantVectorStore.from_existing_collection(
                embedding=embedding_model,
                collection_name="health_report",
                url="http://localhost:6333",
            )

    except Exception:
        return None


def process_query(query: str):
    try:
        vector_store = get_vectorstore()

        if vector_store is None:
            return "⚠️ Please upload a health report first before asking questions."

        search_result = vector_store.similarity_search(query)

        if not search_result:
            return f"⚠️ Sorry, no relevant document found for your query: {query}"

        context = "\n".join(
            [f"page content : {doc.page_content}" for doc in search_result]
        )

        SYSTEM_PROMPT = system_prompt(context)

        response = client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": query},
            ],
            temperature=1.5,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Something went wrong while fetching results: {str(e)}"
