import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# TODO: Remove sidebar

st.title("Welcome!")

st.subheader("Please click on the button below to start with Grader Bot!")


if st.button("START"):
    st.switch_page("pages/assignment_ingest.py")