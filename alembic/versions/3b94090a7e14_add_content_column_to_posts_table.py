"""add content column to posts table

Revision ID: 3b94090a7e14
Revises: 45462a4ee42a
Create Date: 2022-02-12 00:47:47.257005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b94090a7e14'
down_revision = '45462a4ee42a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
