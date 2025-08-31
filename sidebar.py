import streamlit as st


def sidebar_info():
    with st.sidebar:
        st.markdown("## 📋 How to Use")
        st.markdown(
            """
        1. **Upload** your health report (PDF/Image)
        2. **Wait** for processing completion
        3. **Ask** questions about your report
        4. **Get** AI-powered insights
        """
        )

        st.markdown("---")

        st.markdown("## 🔧 Features")
        st.markdown(
            """
        - 📄 **PDF & Image Support**
        - 🧠 **AI Analysis**
        - 💬 **Interactive Chat**
        - 🔍 **Smart Search**
        - 📊 **Report Insights**
        """
        )
        if st.button("🗑️ Delete All Chat"):
            if "messages" in st.session_state:
                st.session_state["messages"] = []
            st.toast("All chat history deleted ✅")
