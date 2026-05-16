# Main Application (main.py) The entry point of the application where routers are included.
from fastapi import FastAPI
from routes import base, data, nlp
from helpers.config import get_settings
from contextlib import asynccontextmanager
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TempleteParser
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)  # connecting to postgres with sqlalchemy
from sqlalchemy.orm import sessionmaker


# @asynccontextmanager
# async def lifespan(app: FastAPI):
# كود الـ Startup (بيتنفذ أول ما السيرفر يقوم)
# هنا ممكن تحطي كود ربط قاعدة البيانات اللي كان في الـ on_event
#   print("Application startup...")
#   yield
# كود الـ Shutdown (بيتنفذ لما السيرفر يقفل)
#    print("Application shutdown...")

app = FastAPI()


@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    # عشان نتواصل مع المونجو والداتا بيز بتاعنا
    # app بخرن فيها ال global variables عشان كله يشوف
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"

    app.db_engine = create_async_engine(postgres_conn, echo=True)

    app.db_client = sessionmaker(
        app.db_engine, expire_on_commit=False, class_=AsyncSession
    )

    app.include_router(nlp.nlp_router)

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(
        settings
    )  # بيكون بيها اللي انا محتاجه

    # generation client
    app.generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND
    )
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = llm_provider_factory.create(
        provider=settings.EMBEDDING_BACKEND
    )
    app.embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_MODEL_SIZE,
    )

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )

    app.vectordb_client.connect()

    app.template_parser = TempleteParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )


@app.on_event("shutdown")
async def shutdown_span():
    app.db_engine.dispose()
    app.vectordb_client.disconnect()


# app.router.lifespan.on_startup.append(startup_span)
# app.router.lifespan.on_shutdown.append(shutdown_span)

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     settings = get_settings()
#     app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
#     app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
#     print("Application startup... Database connected")
#     yield
#     app.mongo_conn.close()
#     print("Application shutdown... Database connection closed")


# app = FastAPI(lifespan=lifespan)

# app.include_router(base.base_router)
# app.include_router(data.data_router)
