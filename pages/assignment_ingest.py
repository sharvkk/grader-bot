import streamlit as st
import pandas as pd
from io import StringIO
from util.textract import load_pdf_text


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    file_path = "data/assignment.pdf"
    with open(file_path, "wb") as file:
        file.write(bytes_data)

    st.session_state["current_assignment"] = load_pdf_text("data/assignment.pdf")

    st.text_area(label = "Extracted text", value = st.session_state.current_assignment, height = 300)


if st.button("Proceed", disabled = uploaded_file is None):
    st.switch_page("pages/configure_solution.py")

