"""'initial'

Revision ID: 1f825ad3c221
Revises: 
Create Date: 2024-04-02 13:26:29.502064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f825ad3c221'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('process',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), server_default='running', nullable=False),
    sa.Column('start_number', sa.Integer(), server_default='0', nullable=False),
    sa.Column('begin_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('finish_date', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('process')
    # ### end Alembic commands ###
