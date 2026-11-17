from datetime import datetime, timezone
from app.domain.entities.treinador import TreinadorResumo
from uuid import UUID, uuid4

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.atleta_esporte import (
    AtletaEsporte,
    AtletaEsporteStatus,
)
from app.domain.entities.esporte import Esporte
from app.domain.repositories.atleta_esporte import AtletaEsporteRepository
from app.infrastructure.database.models import (
    AtletaEsporteModel,
    AtletaModel,
    EsporteModel,
    EsporteTreinadorModel,
    TreinadorModel,
)
from app.infrastructure.repositories.base import BaseRepositoryImpl


class AtletaEsporteRepositoryImpl(
    BaseRepositoryImpl[AtletaEsporte, AtletaEsporteModel],
    AtletaEsporteRepository,
):
    @property
    def model_class(self) -> type[AtletaEsporteModel]:
        return AtletaEsporteModel

    def _to_entity(self, model: AtletaEsporteModel) -> AtletaEsporte:
        return AtletaEsporte(
            id=model.id,
            atleta_id=model.atleta_id,
            esporte_id=model.esporte_id,
            status=AtletaEsporteStatus(model.status),
            criado_em=model.criado_em,
            alterado_em=model.alterado_em,
        )

    def _to_model(self, entity: AtletaEsporte) -> AtletaEsporteModel:
        return AtletaEsporteModel(
            id=entity.id,
            atleta_id=entity.atleta_id,
            esporte_id=entity.esporte_id,
            status=entity.status.value,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
        )

    async def get(self, vinculo_id: UUID) -> AtletaEsporte | None:
        return await super().get(vinculo_id)
    
    async def list_trainers_by_esporte(
        self, esporte_id: UUID
    ) -> list[TreinadorResumo]:
        result = await self.session.execute(
            select(TreinadorModel)
            .join(
                EsporteTreinadorModel,
                EsporteTreinadorModel.treinador_id == TreinadorModel.id,
            )
            .where(EsporteTreinadorModel.esporte_id == esporte_id)
            .order_by(TreinadorModel.nome)
        )
        return [
            TreinadorResumo(
                id=m.id, user_id=m.user_id, nome=m.nome, email=m.email, bio=m.bio
            )
            for m in result.scalars().all()
        ]

    @staticmethod
    def _to_entity_with_names(row: tuple) -> AtletaEsporte:
        model, atleta_nome, esporte_nome = row
        entity = self._to_entity(model)
        return AtletaEsporte(
            id=entity.id,
            atleta_id=entity.atleta_id,
            esporte_id=entity.esporte_id,
            status=entity.status,
            criado_em=entity.criado_em,
            alterado_em=entity.alterado_em,
            atleta_nome=atleta_nome,
            esporte_nome=esporte_nome,
        )

    async def inscrever(self, atleta_id: UUID, esporte_id: UUID) -> AtletaEsporte:
        return await self.solicitar(atleta_id, esporte_id)

    async def solicitar(self, atleta_id: UUID, esporte_id: UUID) -> AtletaEsporte:
        result = await self.session.execute(
            select(AtletaEsporteModel).where(
                AtletaEsporteModel.atleta_id == atleta_id,
                AtletaEsporteModel.esporte_id == esporte_id,
            )
        )
        model = result.scalar_one_or_none()
        agora = datetime.now(timezone.utc)
        if model is not None:
            if model.status == AtletaEsporteStatus.APROVADO.value:
                raise ValueError("O atleta já está vinculado a este esporte.")
            if model.status == AtletaEsporteStatus.PENDENTE.value:
                raise ValueError("Já existe uma solicitação pendente.")
            model.status = AtletaEsporteStatus.PENDENTE.value
            model.alterado_em = agora
        else:
            model = AtletaEsporteModel(
                id=uuid4(),
                atleta_id=atleta_id,
                esporte_id=esporte_id,
                status=AtletaEsporteStatus.PENDENTE.value,
                criado_em=agora,
                alterado_em=agora,
            )
            self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def cancelar_inscricao(self, atleta_id: UUID, esporte_id: UUID) -> None:
        await self.session.execute(
            delete(AtletaEsporteModel).where(
                AtletaEsporteModel.atleta_id == atleta_id,
                AtletaEsporteModel.esporte_id == esporte_id,
            )
        )
        await self.session.commit()

    async def list_by_atleta(self, atleta_id: UUID) -> list[AtletaEsporte]:
        result = await self.session.execute(
            select(AtletaEsporteModel).where(
                AtletaEsporteModel.atleta_id == atleta_id
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_by_esporte(self, esporte_id: UUID) -> list[AtletaEsporte]:
        result = await self.session.execute(
            select(AtletaEsporteModel).where(
                AtletaEsporteModel.esporte_id == esporte_id
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def list_by_atleta_status(
        self, atleta_id: UUID, status: AtletaEsporteStatus
    ) -> list[AtletaEsporte]:
        result = await self.session.execute(
            select(AtletaEsporteModel).where(
                AtletaEsporteModel.atleta_id == atleta_id,
                AtletaEsporteModel.status == status.value,
            )
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def _list_for_trainer(
        self, user_id: UUID, status: AtletaEsporteStatus
    ) -> list[AtletaEsporte]:
        result = await self.session.execute(
            select(AtletaEsporteModel, AtletaModel.nome, EsporteModel.nome)
            .join(AtletaModel, AtletaModel.id == AtletaEsporteModel.atleta_id)
            .join(EsporteModel, EsporteModel.id == AtletaEsporteModel.esporte_id)
            .outerjoin(
                EsporteTreinadorModel,
                EsporteTreinadorModel.esporte_id == EsporteModel.id,
            )
            .outerjoin(
                TreinadorModel,
                TreinadorModel.id == EsporteTreinadorModel.treinador_id,
            )
            .where(
                AtletaEsporteModel.status == status.value,
                or_(
                    EsporteModel.criado_por_user_id == user_id,
                    TreinadorModel.user_id == user_id,
                ),
            )
        )
        return [
            self._to_entity_with_names(row)
            for row in result.unique().all()
        ]

    async def list_pending_for_trainer(
        self, user_id: UUID
    ) -> list[AtletaEsporte]:
        return await self._list_for_trainer(user_id, AtletaEsporteStatus.PENDENTE)

    async def list_approved_for_trainer(
        self, user_id: UUID
    ) -> list[AtletaEsporte]:
        return await self._list_for_trainer(user_id, AtletaEsporteStatus.APROVADO)

    async def get_atleta_id_by_user(self, user_id: UUID) -> UUID | None:
        result = await self.session.execute(
            select(AtletaModel.id).where(AtletaModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def esporte_exists(self, esporte_id: UUID) -> bool:
        result = await self.session.execute(
            select(EsporteModel.id).where(EsporteModel.id == esporte_id)
        )
        return result.scalar_one_or_none() is not None

    async def list_available_esportes(self) -> list[Esporte]:
        result = await self.session.execute(
            select(EsporteModel).order_by(EsporteModel.nome)
        )
        return [
            Esporte(
                id=model.id,
                user_id=model.criado_por_user_id,
                nome=model.nome,
                descricao=model.descricao,
                criado_em=model.criado_em,
                instituicao_id=model.instituicao_id,
                alterado_em=model.alterado_em,
            )
            for model in result.scalars().all()
        ]

    async def trainer_can_manage_esporte(
        self, esporte_id: UUID, user_id: UUID
    ) -> bool:
        result = await self.session.execute(
            select(EsporteModel.id)
            .outerjoin(
                EsporteTreinadorModel,
                EsporteTreinadorModel.esporte_id == EsporteModel.id,
            )
            .outerjoin(
                TreinadorModel,
                TreinadorModel.id == EsporteTreinadorModel.treinador_id,
            )
            .where(
                EsporteModel.id == esporte_id,
                or_(
                    EsporteModel.criado_por_user_id == user_id,
                    TreinadorModel.user_id == user_id,
                ),
            )
        )
        return result.first() is not None

    async def decide(
        self, vinculo_id: UUID, user_id: UUID, status: AtletaEsporteStatus
    ) -> AtletaEsporte:
        result = await self.session.execute(
            select(AtletaEsporteModel).where(
                AtletaEsporteModel.id == vinculo_id
            )
        )
        model = result.scalar_one()
        model.status = status.value
        model.alterado_em = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def cancel_pending(self, vinculo_id: UUID, atleta_id: UUID) -> bool:
        result = await self.session.execute(
            delete(AtletaEsporteModel).where(
                AtletaEsporteModel.id == vinculo_id,
                AtletaEsporteModel.atleta_id == atleta_id,
                AtletaEsporteModel.status == AtletaEsporteStatus.PENDENTE.value,
            )
        )
        await self.session.commit()
        return result.rowcount > 0
