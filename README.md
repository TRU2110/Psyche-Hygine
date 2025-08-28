# Psyche-Hygine

1. Create a Virtual Environment:
  python -m venv venv

2. Activate Virtual Environment:
on windows:-
  venv\Scripts\activate

On macOS/Linux:-
  source venv/bin/activate

3. Install Dependencies:
  pip install flask flask-sqlalchemy flask-restplus

4. Create Database:
  python

5. Inside python shell:
  from app import app, db  # Import both app and db
  with app.app_context():
    db.create_all()
  exit()

6. Run Application:
  python app.py


