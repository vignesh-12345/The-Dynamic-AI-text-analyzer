
import pandas as pd
import PyPDF2
import docx2txt
import tempfile
import os
from io import BytesIO

def extract_text_from_upload(uploaded_file):
    name = uploaded_file.name
    ext = name.split(".")[-1].lower()

    
    try:
        uploaded_file.seek(0)
    except Exception:
        pass

    data = uploaded_file.read()

    # Plain text / code / json
    if ext in ["txt", "py", "json"]:
        try:
            content = data.decode("utf-8")
        except Exception:
            content = data.decode("latin-1")
        return content, [content]

    # CSV
    if ext == "csv":
        try:
            df = pd.read_csv(BytesIO(data), encoding="utf-8")
        except Exception:
            df = pd.read_csv(BytesIO(data), encoding="latin-1")
        display = df.to_string()
        if "text" in df.columns:
            blocks = df["text"].astype(str).tolist()
        else:
            blocks = df.astype(str).agg(" | ".join, axis=1).tolist()
        return display, blocks

    # Excel
    if ext in ["xlsx", "xls"]:
        df = pd.read_excel(BytesIO(data))
        display = df.to_string()
        if "text" in df.columns:
            blocks = df["text"].astype(str).tolist()
        else:
            blocks = df.astype(str).agg(" | ".join, axis=1).tolist()
        return display, blocks

    # PDF
    if ext == "pdf":
        pages = []
        try:
            reader = PyPDF2.PdfReader(BytesIO(data))
            for page in reader.pages:
                pages.append(page.extract_text() or "")
        except Exception:
           
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(data)
                tmp.flush()
                tmp_name = tmp.name
            try:
                reader = PyPDF2.PdfReader(tmp_name)
                for page in reader.pages:
                    pages.append(page.extract_text() or "")
            finally:
                try:
                    os.remove(tmp_name)
                except Exception:
                    pass
        display = "\n\n".join(pages)
        return display, [p for p in pages if p.strip()] or [display]

    # DOCX
    if ext == "docx":
       
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(data)
            tmp.flush()
            tmp_name = tmp.name
        try:
            full_text = docx2txt.process(tmp_name) or ""
        finally:
            try:
                os.remove(tmp_name)
            except Exception:
                pass
        paragraphs = [p for p in full_text.splitlines() if p.strip()]
        display = full_text
        return display, paragraphs if paragraphs else [display]

    return "Unsupported file type", [""]
