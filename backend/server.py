from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
import analyze

load_dotenv()

app = Flask(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return "Backend Live"

@app.route('/get_analysis', methods=['POST'])
def get_analysis():
    question = request.json["question"]
    companies = request.json["companies"]
    data = {}
    for ticker in companies:
        data[ticker] = analyze.get_df(ticker)
    
    final_summary = analyze.llm_analyzer(data, question)
    analyze.store_response(companies, question, final_summary)
    return jsonify({"analysis": final_summary})


if __name__ == '__main__':
    app.run(debug=True)
