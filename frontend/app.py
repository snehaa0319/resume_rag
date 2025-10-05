import streamlit as st
import requests
import os

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL")

st.set_page_config(page_title="ResumeRAG Demo", layout="wide")
st.title("ResumeRAG — Resumé Search & Job Match (Demo)")

# Instructions
with st.expander("Instructions", expanded=True):
    st.markdown("""
- Upload resumes (pdf, docx, txt).  
- Click **Index Resumes** to send them to backend for embedding/indexing.  
- Enter a job description and click **Search**.  
- Top K controls number of results shown.
""")

# Upload resumes
uploaded = st.file_uploader(
    "Upload resumes (multiple)", 
    accept_multiple_files=True, 
    type=["pdf","txt","docx"],
    key="upload_resumes"
)

if st.button("Index Resumes", key="index_button"):
    if not uploaded:
        st.warning("Please upload files first.")
    else:
        with st.spinner("Uploading & indexing..."):
            files = []
            for f in uploaded:
                # f.getvalue() returns bytes
                files.append(("files", (f.name, f.getvalue(), f.type or "application/octet-stream")))
            try:
                resp = requests.post(f"{BACKEND_URL}/index_resumes", files=files, timeout=120)
                st.json(resp.json())
            except Exception as e:
                st.error(f"Upload failed: {e}")

st.markdown("---")
st.header("Search for Matching Resumes")

job_desc = st.text_area(
    "Job description", 
    height=180, 
    placeholder="Paste job description or role requirements here...", 
    key="job_desc_area"
)
top_k = st.slider("Top K matches", 1, 10, 3, key="top_k_slider")

if st.button("Search", key="search_button"):
    if not job_desc.strip():
        st.warning("Provide a job description.")
    else:
        payload = {"job_description": job_desc, "top_k": top_k}
        with st.spinner("Searching..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/query", data=payload, timeout=60)
                if resp.status_code != 200:
                    st.error(f"Backend error: {resp.status_code} {resp.text}")
                else:
                    data = resp.json()
                    if "results" not in data or not data["results"]:
                        st.info("No results found.")
                    else:
                        for r in data["results"]:
                            # Card-style display
                            st.markdown(
                                f"""
                                <div style='border:1px solid #ccc; padding:15px; border-radius:10px; margin-bottom:10px; background:#f9f9f9'>
                                <h4>{r['filename']}</h4>
                                <b>Score:</b> {r['score']:.4f}<br>
                                <b>Snippet:</b> {r['snippet']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
            except Exception as e:
                st.error(f"Search request failed: {e}")
