"""empty message

Revision ID: dfd4e78d02e3
Revises: 5096a599daae
Create Date: 2025-05-05 18:48:33.415953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfd4e78d02e3'
down_revision = '5096a599daae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('financials', schema=None) as batch_op:
        batch_op.add_column(sa.Column('goal3', sa.Numeric(precision=10, scale=2), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('financials', schema=None) as batch_op:
        batch_op.drop_column('goal3')

    # ### end Alembic commands ###
