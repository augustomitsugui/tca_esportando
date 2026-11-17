"""Add owners to institutions, locations and sports."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261113_0015"
down_revision: Union[str, Sequence[str], None] = "20261112_2230"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "instituicoes",
        sa.Column("criado_por_user_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_instituicoes_criado_por_user_id",
        "instituicoes",
        "users",
        ["criado_por_user_id"],
        ["id"],
    )
    op.execute(
        """
        UPDATE instituicoes
        SET criado_por_user_id = (
            SELECT c.user_id
            FROM coordenadores c
            WHERE c.instituicao_id = instituicoes.id
            LIMIT 1
        )
        WHERE criado_por_user_id IS NULL
        """
    )

    op.add_column(
        "locais",
        sa.Column("criado_por_user_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_locais_criado_por_user_id",
        "locais",
        "users",
        ["criado_por_user_id"],
        ["id"],
    )

    op.add_column(
        "esportes",
        sa.Column("criado_por_user_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_esportes_criado_por_user_id",
        "esportes",
        "users",
        ["criado_por_user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_esportes_criado_por_user_id", "esportes", type_="foreignkey"
    )
    op.drop_column("esportes", "criado_por_user_id")
    op.drop_constraint(
        "fk_locais_criado_por_user_id", "locais", type_="foreignkey"
    )
    op.drop_column("locais", "criado_por_user_id")
    op.drop_constraint(
        "fk_instituicoes_criado_por_user_id",
        "instituicoes",
        type_="foreignkey",
    )
    op.drop_column("instituicoes", "criado_por_user_id")
