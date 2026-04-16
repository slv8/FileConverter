from sqlalchemy import UUID, Column, DateTime, String, func, text

from app.storage.db import Base


class FileModel(Base):
    __tablename__ = "files"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))

    name = Column(String(50), nullable=False)

    created_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )
