"""create projects table

Revision ID: 2b3c4d5e6f7g
Revises: 1a2b3c4d5e6f
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b3c4d5e6f7g'
down_revision = '1a2b3c4d5e6f' # <-- Menunjuk ke migrasi 'create_users_table'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('project_link', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('projects')
