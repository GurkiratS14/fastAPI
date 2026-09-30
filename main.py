from fastapi import FastAPI 
from fastapi import HTTPException
from fastapi import Response
from fastapi import Depends 
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel import Session
from random import randint
from datetime import datetime
from typing import Any, Annotated

sqlite_file_name="database.db"
sqlite_url=f"sqlite:///{sqlite_file_name}"

connect_args={"check_same_thread":False}
engine=create_engine(sqlite_url,connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep=Annotated[Session,Depends(get_session)]

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

@app.post("/campaigns",status_code=201)
async def create_campaign(body:dict[str,Any]):

    new : Any ={
        "campaign_id":randint(100,1000),
        "name":body.get("name"),
        "due_date":body.get("due_date"),
        "created_at":datetime.now()
    }

    data.append(new)
    return {"campaign":new}

@app.put("/campaigns/{id}")
async def update_campaign(id:int, body:dict[str,Any]):

    for index, campaign in enumerate(data):
        if campaign.get("campaign_id")==id:

            updated : Any ={
                "campaign_id":id,
                "name":body.get("name"),
                "due_date":body.get("due_date"),
                "created_at": campaign.get("careated_at")
            }

            data[index]=updated
            return {"campaign":updated}
    raise HTTPException(status_code=404)

@app.delete("/campaigns/{id}")
async def delete_campaign(id:int):

    for index, campaign in enumerate(data):
        if campaign.get("campaign_id")==id:
            data.pop(index)
            return Response(status_code=204) 
    raise HTTPException(status_code=404)