from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm, oauth2
from pydantic import BaseModel
from datetime import datetime
from typing import List

class Todo(BaseModel):
    name: str
    due_date: datetime
    description: str

app = FastAPI(title="Todo API")
oauth2_sheme = oauth2.OAuth2PasswordBearer(tokenUrl="token")

list_todo = []

def validate(token: str = Depends(oauth2_sheme)):
    return True

@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token" : form_data.username + "token"}


@app.get("/")
async def home():
    return {"App": "ToDo"}

@app.post("/todo/")
async def create_todo(todo: Todo):
    list_todo.append(todo)
    return todo

@app.get("/todo/", response_model=List[Todo])
async def get_all_todos():
    return list_todo

@app.get("/todo/{id}")
async def get_todo(id: int):
    try:
        return list_todo[id]
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found")

@app.put("/todo/{id}")
async def update_todo(id: int, todo: Todo):
    try:
        list_todo[id] = todo
        return list_todo[id]   
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found")

@app.delete("/todo/{id}")
async def delete_todo(id: int, valid: bool = Depends(validate)):
    try:
        obj = list_todo[id]
        list_todo.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found")

        
#python -m uvicorn main:app --reload
