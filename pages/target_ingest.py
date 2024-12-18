import streamlit as st
from util.textract import load_pdf_text
import os

st.set_page_config(
    page_title="Grader BOT",
    initial_sidebar_state="collapsed"
)

st.title("Upload Assignment to be Graded")

all_items = os.listdir("data/targets")
st.session_state['target_number'] = len(all_items) + 1

uploaded_file = st.file_uploader("Upload target assignment PDF to be graded")
if uploaded_file is not None:

    # TODO: Add option for multiple answer sheets

    bytes_data = uploaded_file.getvalue()
    current_target = "target"

    file_path = "data/targets/" + current_target + ".pdf"
    with open(file_path, "wb") as file:
        file.write(bytes_data)

    st.session_state["current_target"] = load_pdf_text(file_path)
    st.text_area(label = "Extracted text", value = st.session_state.current_target, height = 300)

if st.button("Proceed", disabled = uploaded_file is None):
    st.switch_page("pages/evaluation.py")
