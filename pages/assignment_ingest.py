import asyncio
import streamlit as st
import pandas as pd
from util.textract import load_pdf_text, parse_json
from util.agents import create_load_questions_agent, run_agent

st.set_page_config(
    page_title="Grader BOT",
    initial_sidebar_state="collapsed"
)

st.title("Upload Assignment")
edited_df = None
uploaded_file = st.file_uploader("Upload your pdf document")
if uploaded_file is not None and "questions_json" not in st.session_state:

    bytes_data = uploaded_file.getvalue()

    file_path = "data/assignment.pdf"
    with open(file_path, "wb") as file:
        file.write(bytes_data)

    st.session_state["current_assignment"] = load_pdf_text("data/assignment.pdf")

    input_data = {
        "question": st.session_state["current_assignment"],
    }

    agent = create_load_questions_agent("gpt-4o-mini")
    response = asyncio.run(run_agent(agent, input_data))

    questions_json = parse_json(response["output"])

    st.session_state["questions_json"] = questions_json

if "questions_json" in st.session_state:
    st.subheader("Extracted questions")
    st.text("Below is the list of questions extracted from the document. Edit the scores as per your assignment.")

    df = pd.DataFrame(st.session_state.questions_json["questions"])
    edited_df = st.data_editor(
        df, 
        hide_index = True
    )

if st.button("Proceed", disabled = uploaded_file is None):
    # TODO: Change scale of points
    st.session_state["max_points"] = edited_df["max_points"].to_list()
    st.switch_page("pages/configure_solution.py")

