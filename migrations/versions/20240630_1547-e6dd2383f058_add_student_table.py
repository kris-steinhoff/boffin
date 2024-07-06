"""Add student table

Revision ID: e6dd2383f058
Revises:
Create Date: 2024-06-30 15:47:13.672757

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

from boffin.common.models import PrefixedID

revision: str = "e6dd2383f058"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "student",
        sa.Column("id", PrefixedID(prefix="student"), nullable=False),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("student")
