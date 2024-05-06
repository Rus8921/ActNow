""" 

Revision ID: 00643a48d27b
Revises: a3487f4509c9
Create Date: 2024-04-12 11:09:43.921688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00643a48d27b'
down_revision: Union[str, None] = 'a3487f4509c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('story_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_likes_active'), 'likes', ['active'], unique=False)
    op.create_index(op.f('ix_likes_id'), 'likes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_likes_id'), table_name='likes')
    op.drop_index(op.f('ix_likes_active'), table_name='likes')
    op.drop_table('likes')
    # ### end Alembic commands ###