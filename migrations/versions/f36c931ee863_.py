"""empty message

Revision ID: f36c931ee863
Revises: 
Create Date: 2021-11-04 07:59:00.326176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f36c931ee863'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('nationality', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('specialities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('admins',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('agents',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('nationality_id', sa.Integer(), nullable=False),
    sa.Column('speciality_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nationality_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['speciality_id'], ['specialities.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('contacts',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('nationality_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nationality_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('hideouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('missions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.Column('speciality_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=10), nullable=False),
    sa.Column('starts_at', sa.Date(), nullable=False),
    sa.Column('ends_at', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['speciality_id'], ['specialities.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('targets',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('nationality_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['nationality_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('missions_agents',
    sa.Column('mission_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.user_id'], ),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.PrimaryKeyConstraint('mission_id', 'agent_id')
    )
    op.create_table('missions_contacts',
    sa.Column('mission_id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.user_id'], ),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.PrimaryKeyConstraint('mission_id', 'contact_id')
    )
    op.create_table('missions_hideouts',
    sa.Column('mission_id', sa.Integer(), nullable=False),
    sa.Column('hideout_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hideout_id'], ['hideouts.id'], ),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.PrimaryKeyConstraint('mission_id', 'hideout_id')
    )
    op.create_table('missions_targets',
    sa.Column('mission_id', sa.Integer(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.ForeignKeyConstraint(['target_id'], ['targets.user_id'], ),
    sa.PrimaryKeyConstraint('mission_id', 'target_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('missions_targets')
    op.drop_table('missions_hideouts')
    op.drop_table('missions_contacts')
    op.drop_table('missions_agents')
    op.drop_table('targets')
    op.drop_table('missions')
    op.drop_table('hideouts')
    op.drop_table('contacts')
    op.drop_table('agents')
    op.drop_table('admins')
    op.drop_table('users')
    op.drop_table('types')
    op.drop_table('specialities')
    op.drop_table('countries')
    # ### end Alembic commands ###