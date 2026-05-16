# define the Project model for the mini-rag application take the variables from  the project file in the db_schemas folder and make it compatible with postgresql using sqlalchemy

from .minirag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Project(SQLAlchemyBase):

    __tablename__ = "projects"  # اسم ال table اللي هتتخزن فيه ال data

    project_id = Column(
        Integer, primary_key=True, autoincrement=True
    )  # ال id بتاع ال project
    Project_uuid = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )  # ال uuid بتاع ال project

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )  # تاريخ انشاء ال project
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )  # تاريخ تعديل ال project بيتم بس فحال ال update

    new_dumy_col = Column(Integer, nullable=False)
