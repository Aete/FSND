"""empty message

Revision ID: 77db3f3fa24b
Revises: 
Create Date: 2021-01-01 23:54:38.849692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77db3f3fa24b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('genres', sa.ARRAY(sa.String(length=20)), nullable=False),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=30), nullable=False),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('genres', sa.ARRAY(sa.String(length=20)), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('website', sa.String(length=100), nullable=True),
    sa.Column('image_link', sa.String(length=100), nullable=True),
    sa.Column('facebook_link', sa.String(length=50), nullable=True),
    sa.Column('seeking_talent', sa.Boolean(), nullable=False),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    op.drop_table('Venue')
    op.drop_table('Artist')
    # ### end Alembic commands ###
