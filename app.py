import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- Enter your API key here ---
API_KEY = "YOUR_API_KEY_HERE"

# Configure API
genai.configure(api_key=API_KEY)

# Use Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📄 Hackathon Smart Assistant")

# Sidebar for PDF Upload
with st.sidebar:
    st.header("Upload PDF")
    pdf_docs = st.file_uploader("Upload your PDF file", type=["pdf"])
    
    if st.button("Process"):
        if pdf_docs:
            reader = PdfReader(pdf_docs)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            st.session_state.raw_text = text
            st.success("PDF processed successfully!")

# Main App Logic
if "raw_text" in st.session_state:
    
    if st.button("Generate Summary"):
        response = model.generate_content(
            f"Summarize the following text:\n{st.session_state.raw_text[:8000]}"
        )
        st.markdown(response.text)
    
    user_input = st.text_input("Ask a question based on the PDF:")
    
    if user_input:
        response = model.generate_content(
            f"Context:\n{st.session_state.raw_text[:8000]}\n\nQuestion: {user_input}"
        )
        st.info(response.text)

else:
    st.info("Please upload and process a PDF first.")