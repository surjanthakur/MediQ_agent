<<<<<<< HEAD
🩺 MediQ — AI-Powered Health Report Assistant

Mediq is an AI health assistant that smartly analyzes your medical reports (PDFs, scans) and provides AI-powered explanations for your queries.

⚠️ Disclaimer: This project is a demo/prototype. It does not provide real medical advice and cannot replace a doctor’s consultation.

🚀 Features

📄 Upload Medical Reports → Upload your PDFs.

🤖 Automatic Indexing → Splits the document into vector embeddings and stores them in Qdrant VectorDB.

🔎 Smart Retrieval → Fetches the most relevant chunks based on user queries.

💬 AI-Powered Q&A → Generates context-driven answers from your report.

⚡ Streamlit UI → Simple and interactive frontend.

🏗️ Tech Stack

Frontend → Streamlit

Embeddings → HuggingFace / Groq embeddings

Vector DB → Qdrant

LLM → Groq API (moonshot model) / OpenAI GPT

Backend → Python (LangChain for orchestration)

Containerization → Docker + Docker Compose

📂 Project Structure
Mediq/
│── chat_section.py   
│── docker-compose.yml     
│── main.py
│── retrieval.py
│── requirements.txt
│── docker-compose.yml
│── README.md
│── sidebar.py
│── system_prompt.py

⚙️ Setup Instructions

1️⃣ Clone the Repo

cd mediq


2️⃣ Install Dependencies

pip install -r requirements.txt


3️⃣ Run Qdrant via Docker

docker-compose up -d


This will run Qdrant at http://localhost:6333
.

4️⃣ Run Streamlit App

streamlit run main.py


Upload the document → it gets indexed.
Then run queries about your uploaded health report.

🧠 How It Works

Upload Phase

User uploads a PDF.

The file is split into text chunks.

Chunks are converted into embeddings.

Stored in Qdrant Vector DB.

Query Phase

User asks a question.

Relevant chunks are retrieved from Qdrant.

LLM generates a response using the context.

📌 Example Flow

Upload → blood_test_report.pdf

Ask → “Is my blood sugar level normal or high?”

Mediq Response → “According to your report, your blood sugar level is 160 mg/dL, which is slightly high. Normal fasting sugar is 70–110 mg/dL.”

🛡️ Disclaimer

This is a demo AI project. Not intended for medical use.
Always consult a doctor for real medical decisions.

💡 Future Improvements

✅ Support for image reports (OCR extraction)
✅ Multi-document support
✅ Fine-tuned medical domain models
✅ Deployable SaaS platform

👨‍💻 Author

Developed by Surjan Thakur 🧑‍💻
Currently building AI Agents in Python.
=======
# MediQ_agent
>>>>>>> 8ac60f3413f3b2774f79ecb9af8234191819e482
