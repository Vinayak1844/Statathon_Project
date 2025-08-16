from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import LocalSession, Base, engine, TABLE_NAME

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

@app.get("/api/nss/data")
def get_nss_data(
    state: str = None,
    sector: str = None,
    district: str = None,
    religion: str = None,
    social_group: str = None,
    household_size: str = None,
    panel: str = None,
    quarter: str = None,
    visit: str = None,
    db: Session = Depends(get_db)
):
    base_query = f"SELECT * FROM {TABLE_NAME}"
    conditions = []
    values = {}
    
    # Build conditions based on provided parameters
    if state:
        conditions.append("StateUt_Code = :state")
        values['state'] = state
    
    if sector:
        conditions.append("Sector = :sector")
        values['sector'] = sector
    
    if district:
        conditions.append("District_Code = :district")
        values['district'] = district
    
    if religion:
        conditions.append("Religion = :religion")
        values['religion'] = religion
    
    if social_group:
        conditions.append("Social_Group = :social_group")
        values['social_group'] = social_group
    
    if household_size:
        conditions.append("Household_Size = :household_size")
        values['household_size'] = household_size
    
    if panel:
        conditions.append("Panel = :panel")
        values['panel'] = panel
    
    if quarter:
        conditions.append("Quarter = :quarter")
        values['quarter'] = quarter
    
    if visit:
        conditions.append("Visit = :visit")
        values['visit'] = visit
    
    # Build final query
    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
    else:
        query = base_query
    
    # Execute query
    result = db.execute(text(query), values)
    data = [dict(row._mapping) for row in result]
    
    return {
        "success": True,
        "count": len(data),
        "filters_applied": {k: v for k, v in locals().items() if k not in ['db', 'base_query', 'conditions', 'values', 'query', 'result', 'data'] and v is not None},
        "data": data
    }