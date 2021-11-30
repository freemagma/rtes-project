"""Rename table blank_crossword to blank_crosswords

Revision ID: 537b918adfdc
Revises: 2e5efb8ffbce
Create Date: 2021-11-29 03:57:15.763499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '537b918adfdc'
down_revision = '2e5efb8ffbce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blank_crosswords',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blankcrossword_id'), 'blank_crosswords', ['id'], unique=False)
    op.create_index(op.f('ix_blankcrossword_title'), 'blank_crosswords', ['title'], unique=False)
    op.drop_table('blank_crossword')


def downgrade():
    # Lol this is wrong
    op.create_table('blank_crosswords',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blankcrossword_id'), 'blank_crosswords', ['id'], unique=False)
    op.create_index(op.f('ix_blankcrossword_title'), 'blank_crosswords', ['title'], unique=False)
    op.drop_table('blank_crossword')
