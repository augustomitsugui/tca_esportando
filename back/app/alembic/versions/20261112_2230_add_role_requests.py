"""Add role requests and coordinator institution scope."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261112_2230"
down_revision: Union[str, Sequence[str], None] = "1a654f97011b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "coordenadores",
        sa.Column("instituicao_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_coordenadores_instituicao_id",
        "coordenadores",
        "instituicoes",
        ["instituicao_id"],
        ["id"],
    )
    op.create_table(
        "role_requests",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("requested_role", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("institution_id", sa.UUID(), nullable=True),
        sa.Column("decided_by", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.String(length=1024), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["institution_id"], ["instituicoes.id"]),
        sa.ForeignKeyConstraint(["decided_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "requested_role",
            "status",
            name="uq_role_request_user_role_status",
        ),
    )


def downgrade() -> None:
    op.drop_table("role_requests")
    op.drop_constraint(
        "fk_coordenadores_instituicao_id",
        "coordenadores",
        type_="foreignkey",
    )
    op.drop_column("coordenadores", "instituicao_id")
