"""empty message

Revision ID: 45957d7dffc3
Revises: e9e3b4a79d6c
Create Date: 2023-10-17 07:00:05.532787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45957d7dffc3'
down_revision = 'e9e3b4a79d6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###
