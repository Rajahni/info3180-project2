"""empty message

Revision ID: 6b2a99d650d4
Revises: 9c996865d36c
Create Date: 2023-04-17 23:34:26.568511

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6b2a99d650d4'
down_revision = '9c996865d36c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('biography', sa.String(), nullable=True),
    sa.Column('profile_photo', sa.String(), nullable=True),
    sa.Column('joined_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('follows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('caption', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Follows')
    op.drop_table('Posts')
    op.drop_table('Likes')
    op.drop_table('Users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Users_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('firstname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('lastname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('biography', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('profile_photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('joined_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('Likes',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Likes_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='Likes_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Likes_pkey')
    )
    op.create_table('Posts',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Posts_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('caption', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='Posts_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Posts_pkey')
    )
    op.create_table('Follows',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Follows_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('follower_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], name='Follows_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Follows_pkey')
    )
    op.drop_table('posts')
    op.drop_table('likes')
    op.drop_table('follows')
    op.drop_table('users')
    # ### end Alembic commands ###
