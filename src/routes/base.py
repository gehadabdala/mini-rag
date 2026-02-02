from fastapi import APIRouter, FastAPI, Depends #Depends make the application more efficient 
import os
from helpers.config import get_settings , Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)
@base_router.get("/")
async def welcome(app_setting: Settings = Depends(get_settings)):
    #app_setting = get_settings()

    app_name = app_setting.App_Name
    app_version = app_setting.App_Version

    return {
        "app_name": app_name,
        "app_version": app_version,
    }