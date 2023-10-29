"""empty message

Revision ID: b2fa43391171
Revises: 1d366762a040
Create Date: 2023-10-29 13:10:24.363819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2fa43391171'
down_revision = '1d366762a040'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mining_process', schema=None) as batch_op:
        batch_op.add_column(sa.Column('execution_time', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('mining_process', schema=None) as batch_op:
        batch_op.drop_column('execution_time')

    # ### end Alembic commands ###
