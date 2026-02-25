# NYPD Notices API
- University of Lincoln
- Assignment 2, Full Stack Development
- Directed, Written and Published by Mykyta "Nick' Khomiakov

## Tech Stack
- Python
- FastAPI
- SQL
- Uvicorn
- Pydantic

## Project Structure
```
app/
    main.py
    api/
        routers/
            auth.py
            drivers.py
            notices.py
    core/
        security.py
    database/
        db_raw.py
        notice_base.sql
    schemas/
        auth.py
        drivers.py
        notices.py
README.md
requirements.txt
```

## Running the project
```python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Please use these values in db_raw for respective user and password:
user = "root"
password = "SEPS"