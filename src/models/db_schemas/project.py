from pydantic import BaseModel, Field, field_validator, validator
from bson.objectid import ObjectId
from typing import Optional


class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value):  # static method
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed = True

    # decoraror
    @classmethod
    def get_indexes(cls):
        return [
            {
                # شكل ال index اللي هيرجع
                "key": [("project_id", 1)],
                "name": "project_id_index",
                "unique": True,
            }
        ]
