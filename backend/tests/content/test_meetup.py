from backend.tests.utils import login_user
from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import arrow
import base64
import json
import pytest

pytestmark = pytest.mark.asyncio


async def test_create_meetup(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **USER_DATA)
        await login_user(requester, USER_DATA["username"], USER_DATA["password"])

        binary = b"X" * 1024

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
                    "categories": ["musica"],
                    "subcategories": ["rock", "pop-rock"],
                    "img": {"data": str(base64.b64encode(binary), "utf-8")},
                }
            ),
        )
        assert status == 201
        meetup_id = response["@name"]

        response, status = await requester(
            "GET", f"/db/guillotina/users/masipcat/{meetup_id}",
        )
        assert status == 200

        response, status = await requester(
            "GET", f"/db/guillotina/users/masipcat/{meetup_id}/@download/img",
        )
        assert status == 200
        assert response == binary
