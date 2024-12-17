import asyncio
import streamlit as st
import pandas as pd
from util.textract import load_pdf_text, parse_json
from util.agents import create_load_questions_agent, run_agent


uploaded_file = st.file_uploader("Upload assignment")
if uploaded_file is not None:

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

    print("questions_json", questions_json)
    print("type questions_json", type(questions_json))

    st.subheader("Extracted questions")
    st.text("Below is the list of questions extracted from the document. Edit the scores as per your assignment.")

    edited_df = st.data_editor(
        pd.DataFrame(questions_json["questions"]), 
        hide_index = True
    )

    # st.text_area(label = "Extracted questions", value = questions_json, height = 300)


if st.button("Proceed", disabled = uploaded_file is None):
    st.switch_page("pages/configure_solution.py")

