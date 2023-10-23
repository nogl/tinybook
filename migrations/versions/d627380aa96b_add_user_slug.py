"""add user-slug

Revision ID: d627380aa96b
Revises: 5a6b676aef37
Create Date: 2023-10-09 20:30:45.088988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd627380aa96b'
down_revision = '5a6b676aef37'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', sa.String(length=256), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_table_slug'), ['slug'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_table', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_table_slug'))
        batch_op.drop_column('slug')

    # ### end Alembic commands ###
