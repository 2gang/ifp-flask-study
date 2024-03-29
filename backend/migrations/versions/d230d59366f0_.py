"""empty message

Revision ID: d230d59366f0
Revises: 044f1dd543ea
Create Date: 2022-11-13 19:49:00.973185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd230d59366f0'
down_revision = '044f1dd543ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Post', sa.Column('image', sa.String(length=255), nullable=True))
    op.add_column('User', sa.Column('image', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'image')
    op.drop_column('Post', 'image')
    # ### end Alembic commands ###
