import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

data_folder_path = "data"
targets_folder_path = "data/targets"

if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)
    os.makedirs(targets_folder_path)
    print(f"Folder '{data_folder_path}' created.")

# TODO: Remove sidebar
st.set_page_config(
    page_title="Grader BOT",
    initial_sidebar_state="collapsed"
)

st.title("Welcome!")

st.subheader("Please click on the button below to start with Grader Bot!")


if st.button("START"):
    st.switch_page("pages/assignment_ingest.py")