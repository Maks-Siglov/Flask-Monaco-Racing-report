"""Second remove test migration

Revision ID: a5db753ba978
Revises: 37dedff75b2d
Create Date: 2023-11-07 14:58:54.703126+00:00

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5db753ba978'
down_revision: str | None = '37dedff75b2d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('drivers', 'test_migration')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('drivers', sa.Column('test_migration', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
