import time

from .conftest import (
    TEST_PASSWORD,
    api_request,
    create_institution,
    login,
    database_connection,
)


def unique_email(prefix):
    return f"{prefix}.{time.time_ns()}@example.com"


def test_athlete_registration_creates_profile_and_allows_login():
    email = unique_email("athlete")
    status, body = api_request(
        "/auth/register/athlete",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "nome": "Atleta Teste",
            "ano": 2020,
            "bio": "Bio",
        },
    )
    assert status == 201
    assert body["role"] == "atleta"

    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM atletas a
                JOIN users u ON u.id = a.user_id
                WHERE u.email = %s
                """,
                (email,),
            )
            assert cursor.fetchone()[0] == 1

    login_status, token = login(email)
    assert login_status == 200
    assert api_request("/auth/me", token=token)[1]["profile_id"]


def test_trainer_registration_is_pending_and_duplicate_email_is_rejected():
    institution_id = create_institution(f"Trainer Institution {time.time_ns()}")
    email = unique_email("trainer")
    status, body = api_request(
        "/auth/register/trainer",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "nome": "Treinador Teste",
            "institution_id": str(institution_id),
        },
    )
    assert status == 201
    assert body["role"] == "treinador"

    duplicate_status, _ = api_request(
        "/auth/register/trainer",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "nome": "Duplicado",
            "institution_id": str(institution_id),
        },
    )
    assert duplicate_status == 400

    login_status, token = login(email)
    assert login_status == 200
    assert api_request("/auth/me", token=token)[1]["approval_status"] == "pendente"


def test_coordinator_registration_stores_request_without_creating_institution():
    institution_name = f"Pending Institution {time.time_ns()}"
    email = unique_email("coordinator")
    status, body = api_request(
        "/auth/register/coordinator",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "nome": "Coordenador Teste",
            "institution_name": institution_name,
        },
    )
    assert status == 201
    assert body["role"] == "coordenador"

    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM instituicoes WHERE nome = %s",
                (institution_name,),
            )
            assert cursor.fetchone()[0] == 0
            cursor.execute(
                """
                SELECT status, institution_name
                FROM role_requests r
                JOIN users u ON u.id = r.user_id
                WHERE u.email = %s
                """,
                (email,),
            )
            assert cursor.fetchone() == ("pendente", institution_name)


def test_public_registration_cannot_promote_user_to_admin():
    email = unique_email("public")
    status, body = api_request(
        "/auth/register",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "is_superuser": True,
            "role": "admin",
        },
    )
    assert status == 201
    assert body["is_superuser"] is False
    assert body["role"] == "atleta"


def test_public_institutions_expose_only_selection_fields():
    institution_id = create_institution(f"Public Institution {time.time_ns()}")
    status, institutions = api_request("/instituicoes/public")
    assert status == 200
    institution = next(
        item for item in institutions if item["id"] == str(institution_id)
    )
    assert set(institution) == {"id", "nome"}


def test_athlete_can_update_own_profile():
    email = unique_email("athlete-update")
    status, body = api_request(
        "/auth/register/athlete",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "nome": "Nome Original",
            "ano": 2020,
        },
    )
    assert status == 201
    _, token = login(email)
    profile_id = api_request("/auth/me", token=token)[1]["profile_id"]

    update_status, updated = api_request(
        f"/atletas/{profile_id}",
        {"nome": "Nome Atualizado", "bio": "Nova bio"},
        token,
        method="PUT",
    )
    assert update_status == 200
    assert updated["nome"] == "Nome Atualizado"
    assert updated["bio"] == "Nova bio"
