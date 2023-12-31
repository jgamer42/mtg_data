"""mensaje

Revision ID: e426d8a20280
Revises: 1796f1386276
Create Date: 2023-12-03 10:02:36.208779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e426d8a20280'
down_revision: Union[str, None] = '1796f1386276'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decks', sa.Column('cuantity', sa.Integer(), nullable=False))
    op.add_column('tournaments', sa.Column('link', sa.String(length=250), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournaments', 'link')
    op.drop_column('decks', 'cuantity')
    # ### end Alembic commands ###
