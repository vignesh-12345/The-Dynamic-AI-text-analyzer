# ui_layout.py
import streamlit as st
from Preprocessing import extract_text_from_upload, clean_and_tokenize, preprocess_uploaded_file
def load_ui_style():
    st.markdown(
        """
        <style>
        body {
            background-color: #0f172a;
        }
        .main {
            background-color: #f8fafc;
            padding: 2rem;
            border-radius: 12px;
        }
        h1, h2, h3 {
            color: #0f172a;
        }
        .stButton > button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #1e40af;
        }
        .metric-box {
            background: #e0f2fe;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def header_section():
    st.markdown("## Dynamic Text Analysis Platform")
    st.markdown(
        "Analyze documents, extract insights, and understand text data intelligently."
    )
    st.divider()


def upload_section():
    return st.file_uploader(
        "Upload your document",
        type=["txt", "csv", "xlsx", "pdf", "docx", "py", "json"]
    )


def show_cleaned_text(cleaned_text):
    st.subheader("Cleaned Text Output")
    st.text_area(
        "Processed Text",
        cleaned_text,
        height=250
    )


def show_token_analysis(total_tokens, unique_tokens, freq_df):
    st.subheader("Token Analysis")

    col1, col2 = st.columns(2)
    col1.metric("Total Tokens", total_tokens)
    col2.metric("Unique Tokens", unique_tokens)

    st.markdown("### Most Frequent Tokens")
    st.dataframe(freq_df, use_container_width=True)
