"""Consolidate athlete-sport requests into the association table."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261113_1430"
down_revision: Union[str, Sequence[str], None] = "20261113_0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "atleta_esportes",
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="aprovado",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("atleta_esportes", "status")
