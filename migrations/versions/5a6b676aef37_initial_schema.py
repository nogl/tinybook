"""Initial schema

Revision ID: 5a6b676aef37
Revises: 
Create Date: 2023-10-09 20:14:53.277314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a6b676aef37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('namespace_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', sa.String(length=256), nullable=True))
        batch_op.create_index(batch_op.f('ix_namespace_table_slug'), ['slug'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('namespace_table', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_namespace_table_slug'))
        batch_op.drop_column('slug')

    # ### end Alembic commands ###
