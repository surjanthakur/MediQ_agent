import streamlit as st
from retrieval import process_query
from qdrant_client import QdrantClient


def styling():
    st.markdown(
        """
<style>
.user-message {
  max-width: max-content;
  max-height: max-content;
  padding: 1rem;
  background-color: #3c3d37;
  margin-left: auto;
  margin-top: 1rem;
  border-radius: 20px;
  margin-bottom: 1rem;
}

.assistant-message {
  max-width: max-content;
  max-height: max-content;
  padding: 1rem;
  margin-right: auto;
  border-radius: 20px;
  margin-bottom: 1rem;
}

strong {
 color: #ffd700;
}

</style>
""",
        unsafe_allow_html=True,
    )


def check_collection_exists():
    """Check if the health_report collection exists in Qdrant"""
    try:
        qdrant_client = QdrantClient(url="http://localhost:6333")
        qdrant_client.get_collection("health_report")
        return True
    except:
        st.toast("⚠️ upload report  !!")
        return False


def display_chat_history():
    """Display chat history with custom styling"""

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"""
              <div class="user-message">
                    <strong>You: </strong>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:  # assistant message
            st.markdown(
                f"""
            <div class="assistant-message">
                    <strong>👧mediQ: </strong>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )


def chat_section():
    try:
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        collection_exist = check_collection_exists()

        if collection_exist:

            # 1. Always display old messages first
            display_chat_history()

            # 2. Then take new input
            input_query = st.chat_input("ask abour your report...")

            if input_query:

                # Add user message
                st.session_state.messages.append(
                    {"role": "user", "content": input_query}
                )

                # Process query
                with st.spinner("🤔 thinking..."):
                    result = process_query(input_query)

                    # Add assistant response
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": result,
                        }
                    )

                # 3. Re-display updated history
                display_chat_history()
        else:
            return None

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
