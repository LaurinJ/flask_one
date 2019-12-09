"""new datetime in Kalkulacka

Revision ID: 688fd85f3129
Revises: 
Create Date: 2019-12-08 18:33:46.244726

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '688fd85f3129'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Kalkulacka", sa.Column("date", sa.DateTime, default=datetime.utcnow()))


def downgrade():
    op.drop_column("Kalkulacka", "date")
