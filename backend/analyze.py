from dotenv import load_dotenv
import os
import requests
import analyze
import pandas as pd
from openai import OpenAI


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir)) 
TRANSCRIPTS_DIR = os.path.join(ROOT_DIR, 'data', 'earning-calls')
RESPONSES_FILE = os.path.join(ROOT_DIR, 'data', 'responses.csv')


def get_df(ticker):
    file_path = os.path.join(TRANSCRIPTS_DIR, f'{ticker}_earning_calls.csv')
    
    # Check if the CSV file exists
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return None


def llm_analyzer(data, question):
    client = OpenAI(
        api_key=openai_api_key
    )
    responses = {}
    
    # Loop through each company's data
    for ticker, df in data.items():
        prompt = f"""
        I have earnings call data from the company {ticker}.
        Please analyze the earnings data and give details regarding the following question: {question}. 
        Explain based on the provided earnings data, do not give "No" or "I can't" for an answer. Make it detailed and lengthy
        Below is the earnings data:
        
        """ + df["transcript"].to_string(index=False)
        print("FRI HERE")
        print("Length of Prompt", len(prompt))

        llm_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Save the response
        responses[ticker] = llm_response.choices[0].message.content.strip()
    
    
    # Combine all responses
    combined_analysis = "\n\n".join(f"{ticker}: {response}" for ticker, response in responses.items())
    
    final_prompt = f"""
    You have been provided with the following analysis of the earning reports from different companies:.
    Please summarize this analysis and provide a final answer to the question by comparing {question} and contrasting the analysis.
    Explain based on the provided earnings data/analysis, do not give "No" or "I can't" for an answer. Make it detailed and lengthy, minimum 4 paragraphs
    Combined Analysis is Below
    """ + combined_analysis

    print("Length of Final Prompt", len(final_prompt))

    
    llm_final_comparison = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )

    # Return the final summarized response
    return llm_final_comparison.choices[0].message.content.strip()

def store_response(tickers, question, final_summary):
    data = pd.read_csv(RESPONSES_FILE)

    tickers = ", ".join(tickers)

    # Create a new row with the response data
    new_response = pd.DataFrame({
        "Tickers": [tickers],
        "Question": [question],
        "Response": [final_summary]
    })

    # Append the new response to the DataFrame
    data = pd.concat([data, new_response], ignore_index=True)

    # Save the updated DataFrame back to the CSV
    data.to_csv(RESPONSES_FILE, index=False)