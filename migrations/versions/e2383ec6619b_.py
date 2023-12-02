"""empty message

Revision ID: e2383ec6619b
Revises: f04105c812a1
Create Date: 2023-12-02 15:45:13.499496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2383ec6619b'
down_revision = 'f04105c812a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_products', schema=None) as batch_op:
        batch_op.drop_constraint('transaction_products_itemCode_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'products', ['itemCode'], ['itemCode'], onupdate='CASCADE', ondelete='RESTRICT')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transaction_products', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('transaction_products_itemCode_fkey', 'products', ['itemCode'], ['itemCode'])

    # ### end Alembic commands ###