import streamlit as st
import os
import pandas as pd
from io import StringIO


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir, os.pardir)) 
TRANSCRIPTS_DIR = os.path.join(ROOT_DIR, 'data', 'earning-calls')

def get_companies():
    COMPANIES = {}
    files = os.listdir(TRANSCRIPTS_DIR)
    for file in files:
        if file.endswith('_earning_calls.csv'):
            ticker = file.split('_')[0]
            COMPANIES[ticker] = file
    return COMPANIES

COMPANIES = get_companies()

def load_existing_transcripts():
    """Load the list of available transcripts from the directory."""
    df = pd.DataFrame(list(COMPANIES.items()), 
                      columns=["Company", "Earnings Call"])
    return df

def save_transcript(company_name, ticker, date, transcript):
    """Save the transcript for a company, and append it if the company already exists."""
    file_name = f"{ticker}_earning_calls.csv"
    file_path = os.path.join(TRANSCRIPTS_DIR, file_name)

    new_data = {
        "company": company_name,
        "date": date,
        "transcript": transcript
    }

    
    if company_name.lower() in map(lambda x: x.lower(), COMPANIES.keys()) and os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame(new_data)], ignore_index=True)
        df.to_csv(file_path, index=False)
    else:
        df = pd.DataFrame([new_data])
        df.to_csv(file_path, index=False)

    COMPANIES[company_name] = file_name
    table_load.empty()
    return file_name

def get_transcript(path):
    df = pd.read_csv(path)
    return df

st.title('📂 Access and Upload Earnings Calls')

table_load, table_empty = st.empty(), True
if table_empty:
    table_load.table(load_existing_transcripts())

st.header("Upload or Select Transcript")

company_name = st.text_input("Company Name")
ticker = st.text_input("Company Ticker")
date = st.date_input("Call Date")
uploaded_file = st.file_uploader("Upload Transcript", type="txt")

if uploaded_file and company_name and date:
    uploaded_file_str = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
    file_name = save_transcript(company_name, ticker, date, uploaded_file_str)
    st.success(f"Transcript saved as {file_name} in {TRANSCRIPTS_DIR}")

st.header("Step 2: Access Existing Transcripts")
transcripts = load_existing_transcripts()

if not transcripts.empty:

    # Option to download a specific transcript
    selected_transcript = st.selectbox("Select a transcript to view or download", list(COMPANIES.keys()))
    transcript_path = os.path.join(TRANSCRIPTS_DIR, COMPANIES[selected_transcript])
    if st.button("Open Transcripts"):
        st.dataframe(get_transcript(transcript_path))
        with open(transcript_path, "rb") as f:
            st.download_button(
                label="Download",
                data=f,
                file_name=COMPANIES[selected_transcript],
                mime="text/csv"
            )
else:
    st.write("No earnings calls available.")
