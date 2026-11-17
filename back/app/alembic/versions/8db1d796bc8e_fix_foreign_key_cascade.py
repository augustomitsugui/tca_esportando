```python
"""Fix foreign key cascade on association tables.

Revision ID: 8db1d796bc8e
Revises: 20261113_1530
Create Date: 2026-11-16 07:13:22.859580
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8db1d796bc8e"
down_revision: Union[str, Sequence[str], None] = "20261113_1530"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply ON DELETE CASCADE to association table foreign keys."""

    # atleta_esportes
    op.drop_constraint(
        "atleta_esportes_atleta_id_fkey",
        "atleta_esportes",
        type_="foreignkey",
    )

    op.drop_constraint(
        "atleta_esportes_esporte_id_fkey",
        "atleta_esportes",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "atleta_esportes_atleta_id_fkey",
        "atleta_esportes",
        "atletas",
        ["atleta_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "atleta_esportes_esporte_id_fkey",
        "atleta_esportes",
        "esportes",
        ["esporte_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # instituicao_locais
    op.drop_constraint(
        "instituicao_locais_instituicao_id_fkey",
        "instituicao_locais",
        type_="foreignkey",
    )

    op.drop_constraint(
        "instituicao_locais_local_id_fkey",
        "instituicao_locais",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "instituicao_locais_instituicao_id_fkey",
        "instituicao_locais",
        "instituicoes",
        ["instituicao_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "instituicao_locais_local_id_fkey",
        "instituicao_locais",
        "locais",
        ["local_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # esporte_treinadores
    op.drop_constraint(
        "esporte_treinadores_esporte_id_fkey",
        "esporte_treinadores",
        type_="foreignkey",
    )

    op.drop_constraint(
        "esporte_treinadores_treinador_id_fkey",
        "esporte_treinadores",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "esporte_treinadores_esporte_id_fkey",
        "esporte_treinadores",
        "esportes",
        ["esporte_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.create_foreign_key(
        "esporte_treinadores_treinador_id_fkey",
        "esporte_treinadores",
        "treinadores",
        ["treinador_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Revert ON DELETE CASCADE from association table foreign keys."""

    # atleta_esportes
    op.drop_constraint(
        "atleta_esportes_atleta_id_fkey",
        "atleta_esportes",
        type_="foreignkey",
    )

    op.drop_constraint(
        "atleta_esportes_esporte_id_fkey",
        "atleta_esportes",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "atleta_esportes_atleta_id_fkey",
        "atleta_esportes",
        "atletas",
        ["atleta_id"],
        ["id"],
    )

    op.create_foreign_key(
        "atleta_esportes_esporte_id_fkey",
        "atleta_esportes",
        "esportes",
        ["esporte_id"],
        ["id"],
    )

    # instituicao_locais
    op.drop_constraint(
        "instituicao_locais_instituicao_id_fkey",
        "instituicao_locais",
        type_="foreignkey",
    )

    op.drop_constraint(
        "instituicao_locais_local_id_fkey",
        "instituicao_locais",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "instituicao_locais_instituicao_id_fkey",
        "instituicao_locais",
        "instituicoes",
        ["instituicao_id"],
        ["id"],
    )

    op.create_foreign_key(
        "instituicao_locais_local_id_fkey",
        "instituicao_locais",
        "locais",
        ["local_id"],
        ["id"],
    )

    # esporte_treinadores
    op.drop_constraint(
        "esporte_treinadores_esporte_id_fkey",
        "esporte_treinadores",
        type_="foreignkey",
    )

    op.drop_constraint(
        "esporte_treinadores_treinador_id_fkey",
        "esporte_treinadores",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "esporte_treinadores_esporte_id_fkey",
        "esporte_treinadores",
        "esportes",
        ["esporte_id"],
        ["id"],
    )

    op.create_foreign_key(
        "esporte_treinadores_treinador_id_fkey",
        "esporte_treinadores",
        "treinadores",
        ["treinador_id"],
        ["id"],
    )
```