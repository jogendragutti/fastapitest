"""add last few columns in the posts table

Revision ID: da404fc0823e
Revises: ec4169c84396
Create Date: 2022-02-12 10:40:24.278228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da404fc0823e'
down_revision = 'ec4169c84396'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable= False,server_default = sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
