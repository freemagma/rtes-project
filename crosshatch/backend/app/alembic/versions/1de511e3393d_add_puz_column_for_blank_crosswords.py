"""Add puz column for blank crosswords

Revision ID: 1de511e3393d
Revises: 537b918adfdc
Create Date: 2021-11-30 05:37:34.178032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1de511e3393d'
down_revision = '537b918adfdc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('blank_crosswords', sa.Column('puz', sa.LargeBinary))

def downgrade():
    op.drop_column('blank_crosswords', 'puz')