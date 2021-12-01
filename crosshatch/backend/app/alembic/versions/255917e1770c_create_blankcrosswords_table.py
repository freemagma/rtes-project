"""Create blankcrossword table

Revision ID: 255917e1770c
Revises: 
Create Date: 2021-11-30 07:08:40.635021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255917e1770c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blankcrossword',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('puzfilename', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blankcrossword_id'), 'blankcrossword', ['id'], unique=False)
    op.create_index(op.f('ix_blankcrossword_title'), 'blankcrossword', ['title'], unique=False)


def downgrade():
    op.drop_table('blankcrossword')
