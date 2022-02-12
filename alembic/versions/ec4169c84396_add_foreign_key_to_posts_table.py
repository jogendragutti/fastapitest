"""add foreign key to posts table

Revision ID: ec4169c84396
Revises: 7a606c9f9f01
Create Date: 2022-02-12 01:09:25.036829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec4169c84396'
down_revision = '7a606c9f9f01'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_constraint('posts','owner_id')
    pass
