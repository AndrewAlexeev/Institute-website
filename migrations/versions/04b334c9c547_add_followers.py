"""add followers

Revision ID: 04b334c9c547
Revises: 67a1ad394768
Create Date: 2019-03-19 22:10:44.251579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04b334c9c547'
down_revision = '67a1ad394768'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###