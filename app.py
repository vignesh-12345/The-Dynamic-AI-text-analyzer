import streamlit as st
from UI import load_ui_style, header_section, upload_section, show_cleaned_text, show_token_analysis
from Preprocessing import preprocess_uploaded_file

load_ui_style()
header_section()

uploaded_file = upload_section()

if uploaded_file:
    result = preprocess_uploaded_file(uploaded_file)

    show_cleaned_text("\n\n".join(result["cleaned_text"]))
    show_token_analysis(
        result["total_tokens"],
        result["unique_tokens"],
        result["frequency_df"]
    )
