from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import LocalSession, Base, engine, TABLE_NAME, STATE_TABLE_NAME

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

@app.get("/api/filter")
def get_nss_data(
    state_name: str = None,
    sector: str = None,
    district_name: str = None,
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
    if state_name:
        # First get the state code from the codes table using state name
        state_query = f"SELECT `state_code` FROM {STATE_TABLE_NAME} WHERE `State Name` = :state_name"
        state_result = db.execute(text(state_query), {"state_name": state_name})
        state_code = state_result.fetchone()
        
        if state_code:
            conditions.append("StateUt_Code = :state_code")
            values['state_code'] = state_code[0]
        else:
            return {
                "success": False,
                "error": f"State '{state_name}' not found in codes table"
            }
    
    if sector:
        conditions.append("Sector = :sector")
        values['sector'] = sector
    
    if district_name:
        # First get the district code from the codes table using district name
        district_query = f"SELECT `DISTRICT CODE` FROM {STATE_TABLE_NAME} WHERE `DISTRICT NAME` = :district_name"
        district_result = db.execute(text(district_query), {"district_name": district_name})
        district_code = district_result.fetchone()
        
        if district_code:
            conditions.append("District_Code = :district_code")
            values['district_code'] = district_code[0]
        else:
            return {
                "success": False,
                "error": f"District '{district_name}' not found in codes table"
            }
    
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
    
    filters_applied = {}
    if state_name:
        filters_applied['state_name'] = state_name
    if sector:
        filters_applied['sector'] = sector
    if district_name:
        filters_applied['district_name'] = district_name
    if religion:
        filters_applied['religion'] = religion
    if social_group:
        filters_applied['social_group'] = social_group
    if household_size:
        filters_applied['household_size'] = household_size
    if panel:
        filters_applied['panel'] = panel
    if quarter:
        filters_applied['quarter'] = quarter
    if visit:
        filters_applied['visit'] = visit
    
    return {
        "success": True,
        "count": len(data),
        "filters_applied": filters_applied,
        "data": data
    }