import json
from langchain.document_loaders import PyPDFLoader

def load_pdf_text(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text = " ".join([doc.page_content for doc in documents])
    return text

def parse_json(json_string: str):
    json_string = json_string.replace("```json", "").replace("```", "").strip()
    return json.loads(json_string)