"""add content column to posts table

Revision ID: bead7f2f7e7e
Revises: 523ce49caca0
Create Date: 2023-11-29 19:28:22.942660

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bead7f2f7e7e'
down_revision: Union[str, None] = '523ce49caca0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
