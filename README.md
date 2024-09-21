
# CallCrunch 📊📞

An application designed to streamline and simplify the analysis of earnings calls for tech companies by leveraging the power of data analytics and an LLM-driven Q&A system.

### Powered by [OpenAI](https://openai.com)

***This tool helps you efficiently analyze earnings calls, saving time and reducing information overload.***

## Table of Contents

- [Project Overview](#project-overview)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Project Overview

**CallCrunch** was created to address the challenges of digesting large amounts of information from earnings calls, particularly for tech companies. With the vast number of calls hosted on platforms like SeekingAlpha, it becomes difficult to extract actionable insights quickly. CallCrunch simplifies this process by allowing users to upload, select, and analyze earnings call transcripts using an intuitive frontend and an LLM-powered backend to answer specific questions.

This project integrates data processing and analysis with an interactive frontend to assist users in making more informed decisions in a fraction of the time.

## Directory Structure

Here's an overview of the **CallCrunch** project structure:

- **frontend**: Contains the Streamlit application for user interaction.
    - **pages**: Individual pages of the frontend such as call analysis and transcripts.
- **backend**: Handles the logic and LLM interactions for analyzing the earnings call data.
    - **data**: Stores uploaded earnings call transcripts and questions.
        - **earning-calls**: Directory to store uploaded earnings call CSVs.
        - **questions.csv**: Stores the list of questions asked by the user.
        - **responses.csv**: Stores the responses given by the system to the asked questions.

## Installation

This project is built with **Flask**, **Streamlit**, and **Pandas**.

To set up **CallCrunch** on your local development environment, follow these steps:

### 1. Clone the repository to your machine:

```bash
git clone https://github.com/your-username/callcrunch.git
```

### 2. Install packages and configure environment

- Select/Instantiate a Python Venv

- Install app dependencies:

    ```bash
    pip install -r requirements.txt
    ```

- Configure the necessary environment variables in an `.env` file, including your OpenAI API key.

    ```bash
    OPENAI_API_KEY="your-openai-api-key"
    ```

### 3. Frontend Setup:

- Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

- Install any Streamlit dependencies (if necessary):

    ```bash
    pip install streamlit
    ```

## Usage

### Running the App

You can run **CallCrunch** as follows:

#### **Backend**:

Start the Flask backend server:

```bash
cd backend
flask run
```

#### **Frontend**:

Start the Streamlit frontend app:

```bash
cd frontend
streamlit run call_crunch.py
```

You will now be able to upload transcripts, ask questions, and view responses by interacting with the frontend.

## Features

The main features of **CallCrunch** include:

- **Transcript Management**: Upload or select from existing earnings call transcripts for analysis.
- **LLM-Powered Q&A**: Ask questions about the earnings call and get detailed responses powered by OpenAI's language models.
- **Data Storage**: Automatically stores uploaded transcripts and questions for future use.
- **Interactive Dashboard**: The frontend provides an easy-to-use interface for selecting companies, uploading files, and viewing results.
- **Historical Responses**: Keeps track of previous questions and their corresponding answers for review.

## CallCrunch in action

Watch how **CallCrunch** works and simplifies earnings call analysis:

[Video Demonstration]([https://github.com/user-attachments/assets/eedd154f-c0ff-4a5d-ad8f-02751ea26e14](https://github.com/user-attachments/assets/0cd0a9fe-9d40-4907-b0cc-a2c591fbb72a))

Here you can access the UI though uploads are not functional due to the backend (https://callcrunch.streamlit.app)


