from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return "Backend Live"

if __name__ == '__main__':
    app.run(debug=True)
