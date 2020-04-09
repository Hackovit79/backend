import asyncio
import pytest
import json
import arrow


pytestmark = pytest.mark.asyncio


USER_DATA = {"username": "masipcat", "email": "jordi@masip.cat", "password": "Patata"}


async def register_user(requester, **data):
    response, status = await requester(
        "POST", "/db/guillotina/@register", data=json.dumps(data)
    )
    assert status == 200
    return response


async def login_user(requester, username, password):
    response, status = await requester(
        "POST",
        "/db/guillotina/@login",
        data=json.dumps({"username": username, "password": password}),
    )
    assert status == 200
    token = response["token"]
    return f"Bearer {token}"


async def test_register_user(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **USER_DATA)
        await login_user(requester, USER_DATA["username"], USER_DATA["password"])
        response, status = await requester("GET", "/db/guillotina/users/masipcat",)
        assert status == 200
        assert {"username", "email", "avatar", "description"}.issubset(set(response))


async def test_create_meetup(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **USER_DATA)
        bearer = await login_user(
            requester, USER_DATA["username"], USER_DATA["password"]
        )

        response, status = await requester(
            "POST",
            "/db/guillotina/users/masipcat",
            data=json.dumps(
                {
                    "@type": "Meetup",
                    "title": "Prova",
                    "description": "Prova llargs",
                    "start": arrow.utcnow().format(),
                    "end": arrow.utcnow().shift(hours=1).format(),
                }
            ),
        )
        assert status == 201
        meetup_id = response["@name"]

        response, status = await requester(
            "GET", f"/db/guillotina/users/masipcat/{meetup_id}",
        )
        assert status == 200
