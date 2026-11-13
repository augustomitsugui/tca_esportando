import time

from .conftest import (
    TEST_PASSWORD,
    api_request,
    create_admin,
    create_institution,
    login,
)


def email(prefix):
    return f"{prefix}.{time.time_ns()}@example.com"


def register_coordinator(name):
    address = email(name)
    status, _ = api_request(
        "/auth/register/coordinator",
        {
            "email": address,
            "password": TEST_PASSWORD,
            "nome": name,
            "institution_name": f"Institution {name} {time.time_ns()}",
        },
    )
    assert status == 201
    return address


def approve_coordinator(admin_token, coordinator_email, institution_name):
    pending = api_request("/role-requests/pending/superadmin", token=admin_token)[1]
    request = next(
        item
        for item in pending
        if item["institution_name"] == institution_name
    )
    assert api_request(
        f"/role-requests/{request['id']}/approve", {}, admin_token
    )[0] == 200
    return request


def test_admin_approves_coordinator_and_only_correct_coordinator_approves_trainer():
    admin_email = email("admin")
    create_admin(admin_email)
    admin_status, admin_token = login(admin_email)
    assert admin_status == 200

    first_name = f"First {time.time_ns()}"
    second_name = f"Second {time.time_ns()}"
    first_email = email("coordinator-first")
    second_email = email("coordinator-second")
    for address, name in ((first_email, first_name), (second_email, second_name)):
        assert api_request(
            "/auth/register/coordinator",
            {
                "email": address,
                "password": TEST_PASSWORD,
                "nome": name,
                "institution_name": name,
            },
        )[0] == 201

    pending = api_request("/role-requests/pending/superadmin", token=admin_token)[1]
    first_request = next(item for item in pending if item["institution_name"] == first_name)
    second_request = next(item for item in pending if item["institution_name"] == second_name)
    assert api_request(
        f"/role-requests/{first_request['id']}/approve", {}, admin_token
    )[0] == 200
    assert api_request(
        f"/role-requests/{second_request['id']}/reject",
        {"rejection_reason": "Revisao administrativa"},
        admin_token,
    )[0] == 200

    first_status, first_token = login(first_email)
    assert first_status == 200
    first_institutions = api_request("/instituicoes", token=first_token)
    assert first_institutions[0] == 200
    first_institution_id = first_institutions[1][0]["id"]

    trainer_email = email("trainer")
    trainer_status, trainer_body = api_request(
        "/auth/register/trainer",
        {
            "email": trainer_email,
            "password": TEST_PASSWORD,
            "nome": "Trainer",
            "institution_id": first_institution_id,
        },
    )
    assert trainer_status == 201
    trainer_user_id = trainer_body["id"]
    trainer_pending = api_request(
        "/role-requests/pending/coordinator", token=first_token
    )[1]
    trainer_request = next(
        item
        for item in trainer_pending
        if item["user_id"] == trainer_user_id
    )

    second_status, second_token = login(second_email)
    assert second_status == 200
    assert api_request(
        f"/role-requests/{trainer_request['id']}/approve", {}, second_token
    )[0] == 403
    assert api_request(
        f"/role-requests/{trainer_request['id']}/approve", {}, first_token
    )[0] == 200
    approved_status, approved_token = login(trainer_email)
    assert approved_status == 200
    sport_status, sport = api_request(
        "/esportes",
        {"nome": f"Sport {time.time_ns()}"},
        approved_token,
    )
    assert sport_status == 201
    assert sport["instituicao_id"] == first_institution_id


def test_non_admin_cannot_decide_coordinator_request():
    admin_email = email("admin-non-admin")
    create_admin(admin_email)
    _, admin_token = login(admin_email)
    register_coordinator("coordinator")
    pending = api_request("/role-requests/pending/superadmin", token=admin_token)[1]
    request = next(
        item
        for item in pending
        if item["requested_role"] == "coordenador"
        and item["institution_name"].startswith("Institution coordinator")
    )
    athlete_email = email("athlete")
    assert api_request(
        "/auth/register/athlete",
        {
            "email": athlete_email,
            "password": TEST_PASSWORD,
            "nome": "Athlete",
            "ano": 2022,
        },
    )[0] == 201
    _, athlete_token = login(athlete_email)
    assert api_request(
        f"/role-requests/{request['id']}/approve", {}, athlete_token
    )[0] == 403
