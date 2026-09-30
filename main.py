from fastapi import FastAPI 
from fastapi import HTTPException
from datetime import datetime
from typing import Any

app=FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello world"}

data : Any =[
    {
        "campaign_id":1,
        "name":"Summer Launch",
        "due_date":datetime.now(),
        "created_at":datetime.now()
    },
    {
        "campaign_id":2,
        "name":"Black Friday",
        "due_date":datetime.now(),
        "created_at":datetime.now()
    }
]

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id:int):
    for campaign in data:
        if campaign.get("campaign_id")==id:
            return {"campaign":campaign}
    raise HTTPException(status_code=404)