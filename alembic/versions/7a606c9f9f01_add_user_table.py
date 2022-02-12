"""add user table

Revision ID: 7a606c9f9f01
Revises: 3b94090a7e14
Create Date: 2022-02-12 00:53:39.627365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a606c9f9f01'
down_revision = '3b94090a7e14'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id',sa.Integer(), nullable = False),
    sa.Column('email',sa.String(),nullable = False),
    sa.Column('password',sa.String(),nullable = False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
    server_default=sa.text('now()'),nullable = False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
