"""create logging table

Revision ID: 3fdff904b9a
Revises: None
Create Date: 2013-05-26 20:30:00.255857

"""

# revision identifiers, used by Alembic.
revision = '3fdff904b9a'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import HSTORE

def upgrade():
    op.create_table('logs',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('data', HSTORE))


def downgrade():
    op.drop_tale('logs')
