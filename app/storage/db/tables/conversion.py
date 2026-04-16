from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, func, text

from app.storage.db import Base


class ConversionModel(Base):
    __tablename__ = "conversions"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))

    original_file_id = Column(
        UUID,
        ForeignKey("files.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    converted_file_id = Column(
        UUID,
        ForeignKey("files.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    status = Column(String(50), nullable=False, index=True)
    progress = Column(Integer, nullable=False)
    extension = Column(String(50), nullable=False, index=True)

    started_at = Column(DateTime(timezone=False), nullable=True)
    completed_at = Column(DateTime(timezone=False), nullable=True)

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
