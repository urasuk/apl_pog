"""add models

Revision ID: 00ce6fd3c45d
Revises: 
Create Date: 2021-10-28 14:50:42.676746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00ce6fd3c45d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('cid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('cid')
    )
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('firstname', sa.String(length=30), nullable=True),
    sa.Column('lastname', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=15), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('medicine',
    sa.Column('mid', sa.Integer(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('manufacturer', sa.String(length=30), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('demand', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['category'], ['category.cid'], ),
    sa.PrimaryKeyConstraint('mid')
    )
    op.create_table('order',
    sa.Column('oid', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('shipDate', sa.DateTime(timezone=6), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('orders_medicine',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('medicine_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['medicine_id'], ['medicine.mid'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.oid'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_medicine')
    op.drop_table('order')
    op.drop_table('medicine')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###