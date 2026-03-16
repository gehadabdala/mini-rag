# Main Application (main.py) The entry point of the application where routers are included.
from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager

# @asynccontextmanager
# async def lifespan(app: FastAPI):
# كود الـ Startup (بيتنفذ أول ما السيرفر يقوم)
# هنا ممكن تحطي كود ربط قاعدة البيانات اللي كان في الـ on_event
#   print("Application startup...")
#   yield
# كود الـ Shutdown (بيتنفذ لما السيرفر يقفل)
#    print("Application shutdown...")

# app = FastAPI(lifespan=lifespan)
# Events
# @app.on_event("startup")
# async def startup_db_client():
#    settings = get_settings()
#    #عشان نتواصل مع المونجو والداتا بيز بتاعنا
#    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
#    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

# @app.on_event("shutdown")
# async def shutdown_db_client():
#    app.mongo_conn.close()


# app.include_router(base.base_router)
# app.include_router(data.data_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    print("Application startup... Database connected")
    yield
    app.mongo_conn.close()
    print("Application shutdown... Database connection closed")


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
