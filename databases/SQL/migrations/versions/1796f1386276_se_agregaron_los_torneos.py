"""se agregaron los torneos

Revision ID: 1796f1386276
Revises: c1a5f73f3fb7
Create Date: 2023-11-29 21:58:17.680944

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1796f1386276'
down_revision: Union[str, None] = 'c1a5f73f3fb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('decks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('format', sa.String(length=250), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('player', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tournaments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('format', sa.String(length=250), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('source', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card_deck',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deck', sa.Integer(), nullable=True),
    sa.Column('card', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['deck'], ['decks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('standings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('place', sa.String(length=10), nullable=False),
    sa.Column('deck', sa.Integer(), nullable=True),
    sa.Column('Tournament', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Tournament'], ['tournaments.id'], ),
    sa.ForeignKeyConstraint(['deck'], ['decks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('standings')
    op.drop_table('card_deck')
    op.drop_table('tournaments')
    op.drop_table('decks')
    # ### end Alembic commands ###