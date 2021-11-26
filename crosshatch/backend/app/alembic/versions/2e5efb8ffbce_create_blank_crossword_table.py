"""Create blank crossword table

Revision ID: 2e5efb8ffbce
Revises: 
Create Date: 2021-11-24 23:35:19.779071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2e5efb8ffbce"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'blank_crossword',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
    )


def downgrade():
    pass
