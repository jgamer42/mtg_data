"""mensaje

Revision ID: 20cb5c572bba
Revises: f1141b3ffff5
Create Date: 2023-11-29 21:35:31.067846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20cb5c572bba'
down_revision: Union[str, None] = 'f1141b3ffff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sets', sa.Column('release_date', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sets', 'release_date')
    # ### end Alembic commands ###