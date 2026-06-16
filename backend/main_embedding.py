from typing import List
from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, String, Float, Boolean, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    __abstract__ = True

class Recipes(Base):
    __tablename__ = "recipes"
    __table_args__ = {'extend_existing': True}

    VECTOR_LENGTH = 512

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    ingredients: Mapped[list] = mapped_column(JSONB)
    steps: Mapped[list] = mapped_column(JSONB)
    kcal: Mapped[int] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(72))
    subcategory: Mapped[str] = mapped_column(String(72))
    dish_type: Mapped[str] = mapped_column(String(72))

    ingredient_count: Mapped[int] = mapped_column(Integer, index=True)
    recipe_embedding: Mapped[List[float]] = mapped_column(Vector(VECTOR_LENGTH))

