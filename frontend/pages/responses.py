import streamlit as st
import os
import pandas as pd
from io import StringIO


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir)) 
RESPONSES_FILE = os.path.join(ROOT_DIR, 'data', 'responses.csv')

def load_existing_responses():
    """Load the list of available transcripts from the directory."""
    df = pd.read_csv(RESPONSES_FILE)
    return df


st.title('📂 Q&A History of Earnings Calls')

st.dataframe(load_existing_responses())