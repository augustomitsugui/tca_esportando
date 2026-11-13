import time

from .conftest import TEST_PASSWORD, api_request, create_institution, login


def test_generic_role_request_requires_specialized_profile():
    email = f"athlete.{time.time_ns()}@example.com"
    assert api_request(
        "/auth/register",
        {"email": email, "password": TEST_PASSWORD},
    )[0] == 201
    institution_id = create_institution(f"Institution {time.time_ns()}")
    _, token = login(email)
    status, body = api_request(
        "/role-requests",
        {"requested_role": "treinador", "institution_id": str(institution_id)},
        token,
    )
    assert status == 400
    assert "cadastro especializado" in body["detail"]


def test_pending_trainer_cannot_create_sport():
    institution_id = create_institution(f"Institution {time.time_ns()}")
    email = f"trainer.{time.time_ns()}@example.com"
    assert api_request(
        "/auth/register/trainer",
        {
            "email": email,
            "password": TEST_PASSWORD,
            "nome": "Pending Trainer",
            "institution_id": str(institution_id),
        },
    )[0] == 201
    _, token = login(email)
    assert api_request(
        "/esportes",
        {"nome": "Restricted Sport"},
        token,
    )[0] == 403
