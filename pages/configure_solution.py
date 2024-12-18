import streamlit as st
from util.textract import load_pdf_text

st.set_page_config(
    page_title="Grader BOT",
    initial_sidebar_state="collapsed"
)

st.title("Provide solution")
left, right = st.columns(2)

with left:
    st.subheader("Golden solution")
    uploaded_solution = st.file_uploader("Choose a file", key="golden_upload")
    if uploaded_solution is not None:
        # To read file as bytes:
        bytes_data = uploaded_solution.getvalue()

        file_path = "data/solution.pdf"
        with open(file_path, "wb") as file:
            file.write(bytes_data)

        st.session_state["current_golden_solution"] = load_pdf_text(file_path)

        st.text_area(label = "Extracted text", value = st.session_state.current_golden_solution, height = 300)


with right:
    st.subheader("Textbook / references")
    uploaded_textbook = st.file_uploader("Choose a file", key="textbook_upload")
    if uploaded_textbook is not None:
        
        bytes_data = uploaded_textbook.getvalue()

        file_path = "data/textbook.pdf"
        with open(file_path, "wb") as file:
            file.write(bytes_data)

        st.session_state["current_textbook"] = load_pdf_text(file_path)

        # TODO: Add RAG


if st.button("Proceed", disabled = (uploaded_solution is None) and (uploaded_textbook is None), use_container_width = True):
    st.switch_page("pages/target_ingest.py")