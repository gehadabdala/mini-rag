from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, ForeignKey, Index, Integer, DateTime, func, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
import uuid


class Asset(SQLAlchemyBase):
    __tablename__ = "assets"

    # note=> in postgres بيدعم ان يكون عندي column يتحط فيه dict بس لازم اعرفه ب type json او jsonb عشان اقدر استغل ال indexing اللي بيقدمه postgres في ال jsonb
    # jsonb بيكون اسرع في ال read اما ال json بيكون اسرع في ال write فلو ال asset_config مش هيتعدل كتير يبقى jsonb هو الاختيار الافضل لانه هيخلي ال read اسرع خصوصا ان ال vector db بتحتاج تقرا ال metadata كتير

    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_uuid = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )

    asset_type = Column(String, nullable=False)  # 1 for text, 2 for image, 3 for video
    asset_name = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False)  # size in bytes
    asset_config = Column(
        JSONB, nullable=True
    )  # JSON string that put into metadata of the vector in the vector db

    asset_project_id = Column(
        Integer, ForeignKey("projects.project_id"), nullable=False
    )  # Foreign key to Project.project_id , forignkey => do index
    # عشان اعمل index
    __table_args__ = (
        Index("ix_assets_asset_project_id", "asset_project_id"),
        Index("ix_assets_asset_type", "asset_type"),
    )

    project = relationship("Project", back_populates="assets")

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
