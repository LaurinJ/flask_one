"""pokus

Revision ID: 9e7a47c85b58
Revises: 688fd85f3129
Create Date: 2019-12-08 18:59:30.176186

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '9e7a47c85b58'
down_revision = '688fd85f3129'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("Kalkulacka", sa.Column("date", sa.DateTime, default=datetime.utcnow()))


def downgrade():
    op.drop_column("Kalkulacka", "date")
