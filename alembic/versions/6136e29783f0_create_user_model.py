"""create User model

Revision ID: 6136e29783f0
Revises: 9e7a47c85b58
Create Date: 2019-12-11 21:45:30.845442

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.functions import current_timestamp


# revision identifiers, used by Alembic.
revision = '6136e29783f0'
down_revision = '9e7a47c85b58'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("User",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("username", sa.String, unique=True),
                    sa.Column("password", sa.String),
                    sa.Column("creation_date", sa.DateTime, server_default=current_timestamp()))


def downgrade():
    op.drop_table("User")
