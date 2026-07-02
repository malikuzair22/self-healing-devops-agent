from fastapi import FastAPI
from api.database import init_db, get_incidents

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/status")
def status():
    return {"status": "running"}

@app.get("/incidents")
def incidents():
    rows = get_incidents()
    return {"incidents":rows}

@app.get("/incidents/{incident_id}")
def get_incident_by_id(incident_id: str):
    rows = get_incidents()
    for row in rows:
        if row[0] == incident_id:
           return{"incident": row}
    return {"error": "not found"}
