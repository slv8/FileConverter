# mypy: ignore-errors
"""empty message

Revision ID: dcd0b3a4ec1a
Revises:
Create Date: 2025-06-19 23:52:35.164143

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dcd0b3a4ec1a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "files",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "conversions",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("original_file_id", sa.UUID(), nullable=False),
        sa.Column("converted_file_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("extension", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["converted_file_id"], ["files.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["original_file_id"], ["files.id"], onupdate="CASCADE", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversions_converted_file_id"), "conversions", ["converted_file_id"], unique=False)
    op.create_index(op.f("ix_conversions_extension"), "conversions", ["extension"], unique=False)
    op.create_index(op.f("ix_conversions_original_file_id"), "conversions", ["original_file_id"], unique=False)
    op.create_index(op.f("ix_conversions_status"), "conversions", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_conversions_status"), table_name="conversions")
    op.drop_index(op.f("ix_conversions_original_file_id"), table_name="conversions")
    op.drop_index(op.f("ix_conversions_extension"), table_name="conversions")
    op.drop_index(op.f("ix_conversions_converted_file_id"), table_name="conversions")
    op.drop_table("conversions")
    op.drop_table("files")
