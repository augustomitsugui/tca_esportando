from uuid import uuid4, UUID

from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.application.dtos.user import UserCreateDTO
from app.infrastructure.security.password_hasher import hash_password, verify_password


class UserUseCases:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def criar(self, dto: UserCreateDTO) -> User:
        usuario_existente = await self.repository.buscar_por_email(dto.email)

        if usuario_existente:
            raise ValueError("Email já cadastrado.")

        usuario = User(
            id=uuid4(),
            email=dto.email,
            hashed_password=hash_password(dto.password),
            is_active=True,
            is_verified=False,
        )

        return await self.repository.create(usuario)

    async def buscar_por_email(self, email: str) -> User | None:
        return await self.repository.buscar_por_email(email)

    async def buscar_por_id(self, user_id: UUID) -> User | None:
        return await self.repository.get(user_id)

    async def autenticar(self, email: str, password: str) -> User | None:

        usuario = await self.repository.buscar_por_email(email)

        if usuario is None:
            return None

        if not usuario.is_active:
            return None

        senha_valida = verify_password(password, usuario.hashed_password)

        if not senha_valida:
            return None

        return usuario

    async def alterar_senha(self, user_id: UUID, nova_senha: str) -> User:

        usuario = await self.repository.get(user_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        usuario.hashed_password = hash_password(nova_senha)

        return await self.repository.update(usuario)
