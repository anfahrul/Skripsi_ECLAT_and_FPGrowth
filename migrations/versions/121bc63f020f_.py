"""empty message

Revision ID: 121bc63f020f
Revises: e2383ec6619b
Create Date: 2023-12-17 17:11:17.068120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '121bc63f020f'
down_revision = 'e2383ec6619b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mining_process', schema=None) as batch_op:
        batch_op.add_column(sa.Column('memory_consumtion', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mining_process', schema=None) as batch_op:
        batch_op.drop_column('memory_consumtion')

    # ### end Alembic commands ###
