"""empty message

Revision ID: d7f881f544ff
Revises: e5b833385e33
Create Date: 2024-01-11 13:14:01.725737

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd7f881f544ff'
down_revision = 'e5b833385e33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_password',
               existing_type=mysql.VARCHAR(length=120),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('user_password',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=120),
               existing_nullable=True)

    # ### end Alembic commands ###