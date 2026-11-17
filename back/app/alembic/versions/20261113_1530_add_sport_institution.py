"""Associate sports with their approved trainer institution."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20261113_1530"
down_revision: Union[str, Sequence[str], None] = "20261113_1508"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "esportes",
        sa.Column("instituicao_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_esportes_instituicao_id",
        "esportes",
        "instituicoes",
        ["instituicao_id"],
        ["id"],
    )
    op.execute(
        """
        UPDATE esportes AS e
        SET instituicao_id = rr.institution_id
        FROM role_requests rr
        WHERE e.criado_por_user_id = rr.user_id
          AND rr.requested_role = 'treinador'
          AND rr.status = 'aprovada'
          AND rr.institution_id IS NOT NULL
          AND e.instituicao_id IS NULL
        """
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_esportes_instituicao_id",
        "esportes",
        type_="foreignkey",
    )
    op.drop_column("esportes", "instituicao_id")
