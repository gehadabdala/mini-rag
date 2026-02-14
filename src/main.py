#Main Application (main.py) The entry point of the application where routers are included.
from fastapi import FastAPI
from routes import base
from routes import data

app = FastAPI()
app.include_router(base.base_router) 
app.include_router(data.data_router)   