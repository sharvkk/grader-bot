import streamlit as st
from util.agents import create_grader_agent, run_agent
from util.textract import load_pdf_text
import asyncio

TESTING = True
if TESTING:
    st.session_state["current_target"] = load_pdf_text("data/targets/target.pdf")
    st.session_state["current_assignment"] = load_pdf_text("data/assignment.pdf")
    st.session_state["current_golden_solution"] = load_pdf_text("data/solution.pdf")


if "current_assignment" not in st.session_state:
    st.warning("Cannot find assignment questions document to evaluate!")

if "current_target" not in st.session_state:
    st.warning("Cannot find answer document to evaluate!")

if "current_textbook" and "current_golden_solution" not in st.session_state:
    st.warning("Cannot find goldent answer or textbook!")


st.title("Assignment evaluation")

if "current_golden_solution" in st.session_state:
    input_data = {
        "question": st.session_state["current_assignment"],
        "solution": st.session_state["current_golden_solution"],
        "answer": st.session_state["current_target"],
        # TODO: Add option to change criteria
        "criteria": ["understanding", "explaination"]
    }

    agent = create_grader_agent("gpt-4o-mini")
    response = asyncio.run(run_agent(agent, input_data))

    st.text(response["output"])

