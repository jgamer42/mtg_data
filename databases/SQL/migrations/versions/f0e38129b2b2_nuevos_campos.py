"""nuevos campos

Revision ID: f0e38129b2b2
Revises: c746c27b3a08
Create Date: 2023-10-16 12:04:38.835799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0e38129b2b2'
down_revision: Union[str, None] = 'c746c27b3a08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('reserved_list', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cards', 'reserved_list')
    # ### end Alembic commands ###
