# ResumeRAG: AI-Powered Resume Search and Matching

This project is a Retrieval-Augmented Generation (RAG) system designed to help recruiters and hiring managers quickly find the most relevant resumes for a given job description. It uses AI-powered semantic search to understand the context of both the job requirements and the content of the resumes, providing a ranked list of the best candidates.

## Features

- **Multi-Format Resume Upload**: Supports `.pdf`, `.docx`, and `.txt` file formats.
- **AI-Powered Indexing**: Converts resume content into vector embeddings using OpenAI's models for semantic understanding.
- **Efficient Semantic Search**: Uses FAISS (Facebook AI Similarity Search) for fast and accurate searching, even with a large number of resumes.
- **Job Description Matching**: Ranks resumes based on their semantic similarity to a provided job description.
- **Interactive Web UI**: A simple and intuitive interface built with Streamlit to upload resumes, enter job descriptions, and view ranked results.

## Architecture

The application is composed of two main components:

1.  **Backend (FastAPI)**:
    - An API server that handles the core logic.
    - `/index_resumes`: An endpoint that receives resume files, extracts their text content, generates embeddings via the OpenAI API, and stores them in an in-memory FAISS index.
    - `/query`: An endpoint that takes a job description, generates its embedding, and performs a similarity search against the indexed resumes to find the top matches.

2.  **Frontend (Streamlit)**:
    - A user-friendly web application that provides the interface for the system.
    - Allows users to upload multiple resumes.
    - Provides a text area to paste a job description.
    - Displays the top matching resumes along with a similarity score and a snippet of the resume text.

## Project Structure

```
resume_rag/
├── backend/
│   ├── main.py           # FastAPI application
│   └── requirements.txt  # Backend Python dependencies
└── frontend/
    ├── app.py            # Streamlit application
    └── requirements.txt  # Frontend Python dependencies
```

## Prerequisites

- Python 3.8+
- An OpenAI API Key

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd resume_rag
    ```

2.  **Set up the Backend:**
    - Navigate to the backend directory:
      ```bash
      cd backend
      ```
    - Create and activate a virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Install the required dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Create a `.env` file in the `backend` directory and add your OpenAI API key:
      ```
      OPENAI_API_KEY="your_openai_api_key_here"
      ```

3.  **Set up the Frontend:**
    - Navigate to the frontend directory:
      ```bash
      cd ../frontend
      ```
    - Create and activate a virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Install the required dependencies:
      ```bash
      pip install -r requirements.txt
      ```

## How to Run

You need to run both the backend and frontend servers in separate terminals.

1.  **Run the Backend Server:**
    - In the `backend` directory (with its virtual environment activated):
      ```bash
      uvicorn main:app --reload
      ```
    - The server will be running at `http://localhost:8000`.

2.  **Run the Frontend Application:**
    - In the `frontend` directory (with its virtual environment activated):
      ```bash
      streamlit run app.py
      ```
    - The application will open in your web browser, usually at `http://localhost:8501`.

## How to Use

1.  Open the Streamlit application in your browser.
2.  Click the "Browse files" button to upload one or more resumes (`.pdf`, `.docx`, `.txt`).
3.  Once the files are uploaded, click the **Index Resumes** button. Wait for the confirmation that the files have been indexed.
4.  Paste the job description into the text area.
5.  Adjust the "Top K matches" slider to select how many top resumes you want to see.
6.  Click the **Search** button.
7.  The top matching resumes will be displayed below, showing the filename, a similarity score, and a snippet from the resume.
