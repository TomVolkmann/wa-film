"""isInAbout added

Revision ID: 36c5ac454ccd
Revises: 092b88f1c14c
Create Date: 2019-07-03 14:15:24.860968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36c5ac454ccd'
down_revision = '092b88f1c14c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isInAbout', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'isInAbout')
    # ### end Alembic commands ###
