"""posts table

Revision ID: 7513d91891c9
Revises: 1e482b358435
Create Date: 2024-05-05 21:18:02.799716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7513d91891c9'
down_revision = '1e482b358435'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_first_name')
        batch_op.drop_index('ix_user_last_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('ix_user_last_name', ['last_name'], unique=1)
        batch_op.create_index('ix_user_first_name', ['first_name'], unique=1)

    # ### end Alembic commands ###
