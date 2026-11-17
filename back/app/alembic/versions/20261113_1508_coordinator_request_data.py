"""Store pending coordinator institution data."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261113_1508"
down_revision: Union[str, Sequence[str], None] = "20261113_1430"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("role_requests", sa.Column("institution_name", sa.String(100), nullable=True))
    op.add_column(
        "role_requests",
        sa.Column("institution_description", sa.String(1024), nullable=True),
    )
    op.add_column(
        "role_requests",
        sa.Column("institution_latitude", sa.Float(), nullable=True),
    )
    op.add_column(
        "role_requests",
        sa.Column("institution_longitude", sa.Float(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("role_requests", "institution_longitude")
    op.drop_column("role_requests", "institution_latitude")
    op.drop_column("role_requests", "institution_description")
    op.drop_column("role_requests", "institution_name")
