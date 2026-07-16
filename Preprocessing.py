# preprocessing.py
from extractor import extract_text_from_upload
from cleaner import clean_and_tokenize,token_analysis

__all__ = [
    "extract_text_from_upload",
    "clean_and_tokenize",
    "preprocess_uploaded_file",
]

def preprocess_uploaded_file(uploaded_file, return_tokens=False):
    
    display_text, blocks = extract_text_from_upload(uploaded_file)

    cleaned_blocks = []
    tokens_blocks = []
    for block in blocks:
        clean_text, tokens = clean_and_tokenize(block)
        if clean_text.strip():
            cleaned_blocks.append(clean_text)
            tokens_blocks.append(tokens)

    if return_tokens:
        return display_text, cleaned_blocks, tokens_blocks
    return display_text, cleaned_blocks




__all__ = [
    "extract_text_from_upload",
    "clean_and_tokenize",
    "token_analysis",
    "preprocess_uploaded_file",
]

def preprocess_uploaded_file(uploaded_file):
    """
    Pipeline:
      Extract → Clean → Tokenize → Token Analysis
    """
    display_text, blocks = extract_text_from_upload(uploaded_file)

    cleaned_blocks = []
    all_tokens = []

    for block in blocks:
        clean_text, tokens = clean_and_tokenize(block)
        if clean_text.strip():
            cleaned_blocks.append(clean_text)
            all_tokens.extend(tokens)

    # Token analysis AFTER cleaning
    total_tokens, unique_tokens, top_tokens, freq_df = token_analysis(all_tokens)

    return {
        "display_text": display_text,
        "cleaned_text": cleaned_blocks,
        "tokens": all_tokens,
        "total_tokens": total_tokens,
        "unique_tokens": unique_tokens,
        "top_tokens": top_tokens,
        "frequency_df": freq_df
    }
