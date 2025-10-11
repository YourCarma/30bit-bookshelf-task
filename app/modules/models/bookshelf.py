# pylint: disable=E1136
from datetime import datetime

from sqlalchemy.orm import (
    mapped_column, relationship, Mapped
)
from sqlalchemy import String, ForeignKey, Integer, Table, Text, Column, Enum, UniqueConstraint
from database.base import Base

from modules.items_manager.schemas.units import Kind, Priority, Status


items_tags_association_table  = Table(
    "items_tags_association_table",
    Base.metadata,
    Column("item_id", ForeignKey("items.id")),
    Column("tag_id", ForeignKey("tags.id"))
)

class Users(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    email = mapped_column(String(255), nullable=False, unique=True)
    display_name = mapped_column(String(50), nullable=False)
    items: Mapped[list["Items"]] = relationship("Items", back_populates="user", cascade='save-update, merge, delete', lazy="selectin")
    tags: Mapped[list["Tags"]] = relationship("Tags", back_populates="user", cascade='save-update, merge, delete', lazy="selectin")

class Items(Base):
    __tablename__ = "items"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    title = mapped_column(String(100), nullable=False)
    kind = mapped_column(Enum(Kind), nullable=False, default=Kind.ARTICLE.value)
    status = mapped_column(Enum(Status), nullable=False, default=Status.PLANNED.value)
    priority = mapped_column(Enum(Priority), nullable=False, default=Priority.NORMAL.value)
    notes = mapped_column(Text, default=" ")
    
    user: Mapped[Users] = relationship(
        "Users",
        back_populates="items",
        lazy="selectin"
    )
    
    tags: Mapped[list["Tags"]] = relationship(secondary=items_tags_association_table, back_populates="items", lazy="selectin")
    
class Tags(Base):
    __tablename__ = "tags"
    id = mapped_column(Integer, primary_key= True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"))
    name = mapped_column(String(50), nullable=True)
    
    user: Mapped[Users] = relationship(
            "Users", back_populates="tags", lazy="selectin")
    
    items: Mapped[list["Items"]] = relationship(
        secondary=items_tags_association_table,
        back_populates="tags",
        lazy="selectin"
    )
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='unique_name_for_user'),
    )
    
    