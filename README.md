# Flask Online Voting System

A simple online voting system built with **Python Flask**, **SQLite**, and **Bootstrap**.  
Users can **register**, **login**, and **vote for candidates**, and view real-time results.

---

## Features ✅

- User registration and login with session management  
- Cast votes for candidates  
- Prevent multiple voting per user  
- View voting results with vote count and percentage  
- Responsive UI using Bootstrap  
- Flash messages for success, errors, and notifications  

---

## Technology Stack 🛠️

- **Backend:** Python, Flask  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, Bootstrap  
- **Version Control:** Git & GitHub  

---

## Project Structure 📂

online-voting-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile               # For deployment (Heroku/Gunicorn)
├── .gitignore             # Git ignore rules
├── database.db            # SQLite database (auto-generated)
│
├── templates/             # HTML templates for Flask
│   ├── base.html
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── vote.html
│   └── results.html

----    
## Installation & Setup ⚙️
1. Clone the repository:
```bash
git clone https://github.com/PAkhila123/flask-digital-voting-system-app.git
cd flask-digital-voting-system-app
2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
3. Install dependencies:
```bash
pip install -r requirements.txt
4. Run the Flask app:
```bash
python app.py
5. Open your browser and go to:
```bash
http://127.0.0.1:5000
