from datetime import datetime
import uuid

from sqlalchemy import Boolean, DateTime, Float, String, UUID, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from app.infrastructure.database.session import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    role: Mapped[str] = mapped_column(
        String(length=20), default="atleta", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AtletaModel(Base):
    __tablename__ = "atletas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    ano: Mapped[int] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TreinadorModel(Base):
    __tablename__ = "treinadores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    bio: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CoordenadorModel(Base):
    __tablename__ = "coordenadores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    bio: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class EsporteModel(Base):
    __tablename__ = "esportes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class LocalModel(Base):
    __tablename__ = "locais"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TreinoModel(Base):
    __tablename__ = "treinos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(length=1024), nullable=True)
    data_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    treinador_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("treinadores.id"), nullable=False
    )
    local_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("locais.id"), nullable=False
    )
    esporte_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("esportes.id"), nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class InstituicaoModel(Base):
    __tablename__ = "instituicoes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nome: Mapped[str] = mapped_column(String(length=100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(length=1024), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class InstituicaoLocalModel(Base):
    __tablename__ = "instituicao_locais"

    __table_args__ = (
        UniqueConstraint("instituicao_id", "local_id", name="uq_instituicao_local"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    instituicao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("instituicoes.id"), nullable=False
    )
    local_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("locais.id"), nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class LocalEsporteModel(Base):
    __tablename__ = "local_esportes"

    __table_args__ = (
        UniqueConstraint("local_id", "esporte_id", name="uq_local_esporte"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    local_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("locais.id"), nullable=False
    )
    esporte_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("esportes.id"), nullable=False
    )


class EsporteTreinadorModel(Base):
    __tablename__ = "esporte_treinadores"

    __table_args__ = (
        UniqueConstraint("treinador_id", "esporte_id", name="uix_esporte_treinador"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    treinador_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("treinadores.id"), nullable=False
    )
    esporte_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("esportes.id"), nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AtletaEsporteModel(Base):
    __tablename__ = "atleta_esportes"

    __table_args__ = (
        UniqueConstraint("atleta_id", "esporte_id", name="uq_atleta_esporte"),
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    atleta_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("atletas.id"), nullable=False
    )
    esporte_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("esportes.id"), nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    alterado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
