<<<<<<< HEAD
# 📚 AI Study Planner

An intelligent task planner that breaks down your study goals into daily actionable plans using Google's Gemini AI. Powered by a Flask backend with PostgreSQL and a Streamlit frontend, this tool helps you stay on track with your learning goals.

----------------------------------------------------------------------------------------------------------

## 🚀 Features

- ✨ AI-powered daily task generation using Gemini Pro
- 🗑️ Delete individual tasks or clear all
- ✍️ Add manual tasks
- 🖨️ Export your schedule as a PDF
- 💾 Persistent storage using PostgreSQL
- 🌐 Flask REST API backend
- 🎨 Clean and modern UI with custom CSS

-------------------------------------------------------------------------------------------------------------

## 📂 Folder Structure

project/ 
│ 
├── app.py # Streamlit frontend 
├── backend.py # Flask backend API 
├── .env # Environment variables (e.g. Gemini API key) 
├── requirements.txt # Python dependencies 
├── README.md # Project documentation 
└── .venv/ # Virtual environment (optional, not version-controlled)


---------------------------------------------------------------------------------------------------------------

## 🛠️ Tech Stack

| Layer         | Tech Used                        |
|---------------|----------------------------------|
| ✨ AI         | Google Gemini 1.5 Flash API     |
| 🎨 Frontend   | Streamlit                       |
| 🔙 Backend    | Flask + Flask-CORS              |
| 🗃️ Database   | PostgreSQL + SQLAlchemy         |
| 🐍 Language   | Python                          |


---------------------------------------------------------------------------------------------------------------

## ⚙️ Setup Instructions



1. 🔧 Clone the repository

in bash

git clone https://github.com/your-username/ai-study-planner.git
cd ai-study-planner

------------------------------------

2. 🐍 Create a virtual environment (optional but recommended)

in bash

python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# OR
.venv\Scripts\activate       # Windows

-------------------------------------
3. 📦 Install dependencies

in bash
pip install -r requirements.txt
-------------------------------------
4. 🗝️ Add your environment variables

Create a .env file:
env
GEMINI_API_KEY=your_gemini_api_key_here

please give your api key at its respective place
-------------------------------------
5. 🗃️ Set up PostgreSQL

Make sure PostgreSQL is installed and running. Then create a database:
in sql

CREATE DATABASE studyplanner;



Update the connection URI in backend.py:
in python

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@localhost:5432/studyplanner'

give your username and password at the respective places

--------------------------------------------------------------------------------------------------------------

🧩 How to Run



Step 1: Run the backend (Flask)
in bash

python backend.py

---------------------------

Step 2: Run the frontend (Streamlit)
In another terminal:
in bash

streamlit run app.py


---------------------------------------------------------------------------------------------------------------

🧪 Example Prompt
"Prepare for DBMS external in 5 days"

🔮 The AI will generate a breakdown like:

Day 1: Study ER diagrams, keys, and normalization
Day 2: Learn SQL basics and queries
...
These are automatically saved as tasks in your planner.

---------------------------------------------------------------------------------------------------------------

📄 PDF Export
Click "📄 Download Schedule as PDF" to get a printable version of your current study plan.

---------------------------------------------------------------------------------------------------------------
=======
# Ai-Study-Planner
>>>>>>> 1e375b482bf05c4a479da377e8e874dc1d1aeb3b
