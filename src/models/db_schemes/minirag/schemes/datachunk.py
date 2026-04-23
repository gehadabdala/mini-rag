from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, ForeignKey, Index, Integer, DateTime, func, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel
import uuid


class DataChunk(SQLAlchemyBase):

    __tablename__ = "chunks"

    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_uuid = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    chunk_metadata = Column(
        JSONB, nullable=False
    )  # JSON string that put into metadata of the vector in the vector db
    chunk_order = Column(
        Integer, nullable=False
    )  # Ensure chunk_order is a non-negative integer

    chunk_project_id = Column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )  # Foreign key to Project.project_id
    chunk_asset_id = Column(
        Integer, ForeignKey("assets.asset_id"), nullable=False
    )  # Foreign key to Asset.asset_id

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )  # تاريخ انشاء ال project
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )  # تاريخ تعديل ال project بيتم بس فحال ال update

    project = relationship("Project", back_populates="chunks")
    asset = relationship("Asset", back_populates="chunks")

    __table_args__ = (
        Index("ix_chunks_chunk_project_id", "chunk_project_id"),
        Index("ix_chunks_chunk_asset_id", "chunk_asset_id"),
    )


class RetrivedDocument(BaseModel):
    text: str
    score: float
