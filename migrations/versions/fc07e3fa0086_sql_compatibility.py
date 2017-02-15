"""sql compatibility

Revision ID: fc07e3fa0086
Revises: 7f317474332d
Create Date: 2017-01-30 16:09:53.367166

"""

# revision identifiers, used by Alembic.
revision = 'fc07e3fa0086'
down_revision = '7f317474332d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.alter_column('ip',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=256),
               existing_nullable=True)
        batch_op.alter_column('ua',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=2048),
               existing_nullable=True)
        batch_op.alter_column('user',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=256),
               existing_nullable=True)
        batch_op.alter_column('uuid',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=256),
               existing_nullable=True)

    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('task',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=256),
               existing_nullable=True)
        batch_op.alter_column('user',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=256),
               existing_nullable=True)
        batch_op.alter_column('uuid',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=256),
               existing_nullable=True)

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('uuid',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('user',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('task',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.alter_column('uuid',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('user',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('ua',
               existing_type=sa.String(length=2048),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('ip',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    ### end Alembic commands ###