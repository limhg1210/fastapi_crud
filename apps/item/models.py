from __future__ import annotations

import json
from typing import Optional

from apps.item.schemas import ItemCreate, ItemUpdate
from config.database import Base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    @classmethod
    def create(cls, schema: ItemCreate) -> Item:
        return cls(name=schema.name, content=schema.content)

    @classmethod
    def from_json(cls, item_json: str):
        item_dict = json.loads(item_json)
        return cls(
            id=item_dict["id"],
            created=datetime.fromisoformat(item_dict["created"]),
            name=item_dict["name"],
            content=item_dict["content"]
        )

    def update(self, schema: ItemUpdate) -> None:
        self.name = schema.name
        self.content = schema.content

    def to_json(self):
        return json.dumps(
            {
                "id": self.id,
                "created": str(self.created),
                "name": self.name,
                "content": self.content,
            },
            ensure_ascii=False
        )
