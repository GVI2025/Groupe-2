"""Init

Revision ID: 47c9cfba7cb6
Revises:
Create Date: 2025-06-06 20:21:35.657863

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "47c9cfba7cb6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "salles",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("nom", sa.String(), nullable=False),
        sa.Column("capacite", sa.Integer(), nullable=False),
        sa.Column("localisation", sa.String(), nullable=False),
        sa.Column("disponible", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "reservations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("salle_id", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("heure", sa.Time(), nullable=False),
        sa.Column("utilisateur", sa.String(), nullable=False),
        sa.Column("commentaire", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["salle_id"],
            ["salles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("reservations")
    op.drop_table("salles")
    # ### end Alembic commands ###
