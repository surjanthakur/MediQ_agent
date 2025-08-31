import streamlit as st
import tempfile
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from chat_section import chat_section, styling
from sidebar import sidebar_info


# Page configuration
st.set_page_config(
    page_title="HealthLens — AI Health Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 2rem;
        margin-bottom: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def document_uploading():
    st.markdown(
        """
    <div class="main-header">
        <h1>🥼 MediQ</h1>
        <h3>AI-Powered Health Report Assistant</h3>
        <p>Upload your medical reports and get instant AI-powered insights</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("## 📤 Upload Your Health Report")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "after upload report it takes few sec..", type=["pdf"]
        )

    with col2:
        st.markdown("### 📊 Supported Formats")
        st.markdown(
            """
        - 📄 **PDF** - Lab reports, prescriptions
        - 🖼️ **Images** - Scanned documents
        - 📋 **Medical** - Any health document
        """
        )
        st.markdown(
            "<hr>",
            unsafe_allow_html=True,
        )

    if uploaded_file and "file_uploaded" not in st.session_state:
        try:
            with st.spinner("🔄 Processing your health report..."):
                ext = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_path = temp_file.name

                # load docs
                loader = PyPDFLoader(temp_path)
                docs = loader.load()

                # split texts
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=200,
                    chunk_overlap=50,
                )
                split_docs = text_splitter.split_documents(docs)

                # embeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-mpnet-base-v2",
                )
                qdrant_client = QdrantClient(url="http://localhost:6333", port=6333)
                try:
                    if qdrant_client.get_collection("health_report"):
                        qdrant_client.delete_collection("health_report")
                except:
                    pass

                # vector store
                QdrantVectorStore.from_documents(
                    documents=split_docs,
                    embedding=embeddings,
                    collection_name="health_report",
                    url="http://localhost:6333",
                )

                st.toast("✅ file load successfully")

                st.session_state.chat_history = []
                st.session_state.file_uploaded = True

                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except:
            st.error("oops ! something went wrong with file uploader")


# Run the app
styling()
sidebar_info()
document_uploading()
chat_section()
