# 🤖 AI Job Tracker

AI Job Tracker is a Python-based application designed to help users track and manage job opportunities in one place. It provides a simple interface for managing job information and uses AI-based features to make the job-tracking process easier and more organized.

## 🚀 Features

* Add and manage job opportunities
* Track job application status
* Store important job details
* AI-powered job-related assistance
* Simple and user-friendly interface

## 🛠️ Technologies Used

* Python
* Streamlit
* AI / Gemini API
* Pandas
* SQLite
* HTML & CSS

## 📁 Project Structure

```text
AI-Job-Tracker/
│
├── app.py
├── requirements.txt
├── .env
└── venv/
```

> Note: `.env` and `venv` should not be uploaded to GitHub. The `.env` file contains private API credentials, and `venv` contains the local Python virtual environment.

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Job-Tracker.git
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install required packages

```bash
pip install -r requirements.txt
```

### 5. Add API Key

Create a `.env` file and add your API key:

```text
GEMINI_API_KEY=your_api_key_here
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Security

API keys and other sensitive information are stored in environment variables and should not be uploaded to GitHub.

## 👨‍💻 Author

**Yash Maniyar**

MCA Student | Python & Data Analytics Enthusiast
