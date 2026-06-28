"""initial schema: meeting, action_item, nugget, person

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-28

Mirrors the SQLModel models in `backend/models/`. After Postgres is up, verify
parity with the models by running `alembic upgrade head` followed by
`alembic revision --autogenerate -m "check"` — the autogenerate diff should be empty.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "meeting",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("transcript", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("summary", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("topics", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_meeting_title"), "meeting", ["title"], unique=False)
    op.create_index(
        op.f("ix_meeting_created_at"), "meeting", ["created_at"], unique=False
    )

    op.create_table(
        "action_item",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("owner", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("priority", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("done", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["meeting_id"], ["meeting.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_action_item_meeting_id"), "action_item", ["meeting_id"], unique=False
    )

    op.create_table(
        "nugget",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("category", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("speaker", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(["meeting_id"], ["meeting.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_nugget_meeting_id"), "nugget", ["meeting_id"], unique=False
    )

    op.create_table(
        "person",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meeting_id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("mentions", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["meeting_id"], ["meeting.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_person_meeting_id"), "person", ["meeting_id"], unique=False)
    op.create_index(op.f("ix_person_name"), "person", ["name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_person_name"), table_name="person")
    op.drop_index(op.f("ix_person_meeting_id"), table_name="person")
    op.drop_table("person")

    op.drop_index(op.f("ix_nugget_meeting_id"), table_name="nugget")
    op.drop_table("nugget")

    op.drop_index(op.f("ix_action_item_meeting_id"), table_name="action_item")
    op.drop_table("action_item")

    op.drop_index(op.f("ix_meeting_created_at"), table_name="meeting")
    op.drop_index(op.f("ix_meeting_title"), table_name="meeting")
    op.drop_table("meeting")
