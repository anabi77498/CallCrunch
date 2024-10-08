import streamlit as st
import pandas as pd
import os
import requests

# Page configuration
st.set_page_config(
    page_title="Call Cruncher",
    page_icon="📊",
    layout="wide"
)

if 'selected_question' not in st.session_state:
    st.session_state.selected_question = None  
if 'selected_companies' not in st.session_state:
    st.session_state.selected_question = None 


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir)) 
TRANSCRIPTS_DIR = os.path.join(ROOT_DIR, 'data', 'earning-calls')
QUESTIONS_FILE = os.path.join(ROOT_DIR, 'data', 'questions.csv')

def get_companies():
    COMPANIES = {}
    files = os.listdir(TRANSCRIPTS_DIR)
    for file in files:
        if file.endswith('_earning_calls.csv'):
            ticker = file.split('_')[0]
            COMPANIES[ticker] = file
    return COMPANIES

COMPANIES = get_companies()

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        return pd.read_csv(QUESTIONS_FILE)['Question'].tolist()
    return []

def load_companies():
    return COMPANIES

def update_questions(question):
        
    question = pd.DataFrame({"Question": [question]})
    existing_df = pd.read_csv(QUESTIONS_FILE) if os.path.exists(QUESTIONS_FILE) else pd.DataFrame(columns=['Question'])
    
    updated_df = pd.concat([existing_df, question], ignore_index=True).drop_duplicates(subset=['Question'])
    
    updated_df.to_csv(QUESTIONS_FILE, index=False)

st.title('📊 CallCruncher')

st.header("Select Company Tags")
company_tags = load_companies()
selected_companies = st.multiselect("Select Companies", company_tags)

# Display selected companies
st.write(f"Selected Companies: {', '.join(selected_companies) if selected_companies else 'None selected'}")

st.header("Ask a Question")
existing_questions = load_questions()

# Show existing questions
st.write("Select from existing questions:")
selected_question = st.selectbox("Select a question", existing_questions)

# Input a new question
new_question = st.text_input("Or ask a new question")

if st.button("Submit Question"):
    if new_question:
        update_questions(new_question)
        st.session_state["selected_question"] = new_question
    else:
        st.session_state["selected_question"] = selected_question
    st.session_state["selected_companies"] = selected_companies
    companies = ", ".join(st.session_state["selected_companies"])
    st.success(f"Question: {st.session_state['selected_question']} \n\nFor {companies}")

    if st.session_state["selected_question"] and st.session_state["selected_companies"]:
        payload = {
            "question": st.session_state["selected_question"],
            "companies": st.session_state["selected_companies"]
        }

        response = requests.post("http://127.0.0.1:5000/get_analysis", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.markdown("### Response:")
            st.write(result["analysis"])
        else:
            st.write("Error: Could not get a response from the backend")
    else:
        st.write("Please select both questions and companies.")