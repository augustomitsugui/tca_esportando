import json
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid

import psycopg
from fastapi_users.password import PasswordHelper


BASE_URL = os.getenv("TEST_BASE_URL", "http://127.0.0.1:8000")
TEST_PASSWORD = "Password123!"


def api_request(path, payload=None, token=None, form=False, method=None):
    headers = {}
    data = None
    request_method = method or "GET"
    if payload is not None:
        data = (
            urllib.parse.urlencode(payload).encode()
            if form
            else json.dumps(payload).encode()
        )
        headers["Content-Type"] = (
            "application/x-www-form-urlencoded" if form else "application/json"
        )
        request_method = method or "POST"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers=headers,
        method=request_method,
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        try:
            body = json.loads(error.read())
        except json.JSONDecodeError:
            body = {}
        return error.code, body


def login(email):
    status, body = api_request(
        "/auth/jwt/login",
        {"username": email, "password": TEST_PASSWORD},
        form=True,
    )
    return status, body.get("access_token")


def database_connection():
    return psycopg.connect(
        "host=db port=5432 dbname=fastapi_db user=post_user password=post_pass"
    )


def create_institution(name):
    institution_id = uuid.uuid4()
    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO instituicoes (id, nome, criado_em, alterado_em)
                VALUES (%s, %s, now(), now())
                """,
                (institution_id, name),
            )
    return institution_id


def create_admin(email):
    password_hash = PasswordHelper().hash(TEST_PASSWORD)
    with database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users
                    (id, email, hashed_password, role, is_active, is_superuser, is_verified)
                VALUES (%s, %s, %s, 'atleta', true, true, true)
                """,
                (uuid.uuid4(), email, password_hash),
            )
