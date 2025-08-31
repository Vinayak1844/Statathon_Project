from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import LocalSession, Base, engine, TABLE_NAME, STATE_TABLE_NAME
from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# In-memory chat sessions (keyed by user_id or "default")
chat_sessions = {}



Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    
    # Create a clean filters dictionary with only the filter parameters
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

class ChatRequest(BaseModel):
    user_id: str = "default"
    message: str



import json
import re

def extract_filters_from_message(message: str):
    prompt = f"""
    You are a strict JSON parser. Convert the user request into a JSON object 
    with only these keys if present:
    state_name, sector, district_name, religion, social_group,
    household_size, panel, quarter, visit.

    - Return only valid JSON.
    - Do not include explanations, extra text, or code fences.
    - If a key is not mentioned, omit it.
    
    Example:
    Input: "Show me urban households in Bihar that are Hindu"
    Output: {{"state_name": "Bihar", "sector": "Urban", "religion": "Hindu"}}

    Now parse this message:
    "{message}"
    """

    result = model.generate_content(prompt)

    # Some Gemini SDKs return `result.text()` vs `.text`
    try:
        text = result.text.strip()
    except TypeError:
        text = result.text().strip()

    # Clean up common junk (like ```json ... ```)
    text = re.sub(r"^```[a-zA-Z]*\n", "", text)  # remove opening code fence
    text = re.sub(r"\n```$", "", text)           # remove closing code fence

    try:
        filters = json.loads(text)
        return filters
    except Exception as e:
        print("Failed to parse filters:", text, e)
        return {}




@app.post("/chat")
def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    user_id = req.user_id
    message = req.message

    # get filters from Gemini
    filters = extract_filters_from_message(message) or {}

    # pass filters into your existing filter function
    data = get_nss_data(
        state_name=filters.get("state_name"),
        sector=filters.get("sector"),
        district_name=filters.get("district_name"),
        religion=filters.get("religion"),
        social_group=filters.get("social_group"),
        household_size=filters.get("household_size"),
        panel=filters.get("panel"),
        quarter=filters.get("quarter"),
        visit=filters.get("visit"),
        db=db
    )

    # Ensure reply is never blank
    reply_text = f"Applied filters: {filters if filters else 'none'} | Found {data['count']} records"

    return {
        "reply": reply_text,
        "filters": filters,
        "data": data["data"]
    }
