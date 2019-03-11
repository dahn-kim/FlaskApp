"""empty message

Revision ID: cf6d7ebb8597
Revises: 244c00cc05db
Create Date: 2019-02-25 14:20:05.857762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf6d7ebb8597'
down_revision = '244c00cc05db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_posted', sa.DateTime(), nullable=False))
        batch_op.drop_column('publish_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('publish_date', sa.DATETIME(), nullable=False))
        batch_op.drop_column('date_posted')

    # ### end Alembic commands ###
