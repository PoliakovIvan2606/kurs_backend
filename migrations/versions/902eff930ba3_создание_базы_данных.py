"""Создание базы данных

Revision ID: 902eff930ba3
Revises: 
Create Date: 2024-05-21 22:26:29.029041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '902eff930ba3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accident',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.String(), nullable=False),
    sa.Column('type_of_incident', sa.String(), nullable=False),
    sa.Column('place', sa.String(), nullable=False),
    sa.Column('brands_of_affected_cars', sa.String(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('machine_type', sa.String(), nullable=False),
    sa.Column('summary', sa.String(), nullable=False),
    sa.Column('number_of_victims', sa.Integer(), nullable=False),
    sa.Column('amount_of_damage', sa.Integer(), nullable=False),
    sa.Column('cause', sa.String(), nullable=False),
    sa.Column('road_conditions', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('area', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('supervisor', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=10), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('make', sa.String(), nullable=False),
    sa.Column('date_of_issue', sa.Integer(), nullable=False),
    sa.Column('engine_capacity', sa.Integer(), nullable=False),
    sa.Column('engine_number', sa.String(length=17), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('vehicle_type', sa.String(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('technical_inspection', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hijacking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['number'], ['car.number'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hijacking')
    op.drop_table('car')
    op.drop_table('organization')
    op.drop_table('accident')
    # ### end Alembic commands ###
