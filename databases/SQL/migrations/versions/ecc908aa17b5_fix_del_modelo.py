"""fix del modelo


Revision ID: ecc908aa17b5
Revises: e426d8a20280
Create Date: 2023-12-03 10:14:58.489296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecc908aa17b5'
down_revision: Union[str, None] = 'e426d8a20280'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card_deck', sa.Column('cuantity', sa.Integer(), nullable=False))
    op.drop_column('decks', 'cuantity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decks', sa.Column('cuantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('card_deck', 'cuantity')
    # ### end Alembic commands ###