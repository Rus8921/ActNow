"""post content list

Revision ID: 17a8a6a3c4ee
Revises: 7f0bf6755e19
Create Date: 2024-04-15 12:17:59.816809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17a8a6a3c4ee'
down_revision: Union[str, None] = '7f0bf6755e19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_subscriptions_id', table_name='subscriptions')
    op.drop_table('subscriptions')
    op.add_column('post', sa.Column('typing.List', sa.String(), nullable=True))
    op.create_index(op.f('ix_post_typing.List'), 'post', ['typing.List'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_typing.List'), table_name='post')
    op.drop_column('post', 'typing.List')
    op.create_table('subscriptions',
    sa.Column('subscriber_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('subscribed_to_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['subscribed_to_id'], ['users.id'], name='subscriptions_subscribed_to_id_fkey'),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], name='subscriptions_subscriber_id_fkey'),
    sa.PrimaryKeyConstraint('subscriber_id', 'subscribed_to_id', name='subscriptions_pkey')
    )
    op.create_index('ix_subscriptions_id', 'subscriptions', ['id'], unique=False)
    # ### end Alembic commands ###