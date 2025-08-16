from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import LocalSession, Base, engine,Tablename

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def Home_Page():
    return {"message": "Welcome to the Statathon Project!"}

@app.get("/users/filter")
def filter_users(request: Request, db: Session = Depends(get_db)):
    filters = dict(request.query_params)  # this will take params from URL
    base_query = f"SELECT * FROM {Tablename}"
    conditions = []
    values = []

    for key, value in filters.items():
        conditions.append(f"{key} = :{key}")   
        
        values.append((key, value))

    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
    else:
        query = base_query

    result = db.execute(text(query), dict(values))
    return [dict(row._mapping) for row in result]