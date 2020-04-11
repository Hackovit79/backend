from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import arrow
import asyncio
import json
import pytest

pytestmark = pytest.mark.asyncio


async def test_user_is_public(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **{**USER_DATA, "username": "user1"})
        await register_user(requester, **{**USER_DATA, "username": "user2"})

        response, status = await requester(
            "POST",
            "/db/guillotina/users/user1",
            data=json.dumps(
                {
                    "@type": "Meetup",
                    "title": "Prova 1",
                    "description": "Prova llarga",
                    "start": arrow.utcnow().format(),
                    "end": arrow.utcnow().shift(hours=1).format(),
                    "categories": ["musica"],
                    "subcategories": ["hard-rock"],
                }
            ),
        )
        response, status = await requester(
            "POST",
            "/db/guillotina/users/user2",
            data=json.dumps(
                {
                    "@type": "Meetup",
                    "title": "Prova 2",
                    "description": "Prova llarga",
                    "start": arrow.utcnow().format(),
                    "end": arrow.utcnow().shift(hours=1).format(),
                    "categories": ["musica"],
                    "subcategories": ["rock"],
                }
            ),
        )
        assert status == 201

        # Wait until guillotina sends documents to ES
        await asyncio.sleep(2)

        response, status = await requester(
            "GET", "/db/guillotina/@meetup-filter", authenticated=False
        )
        assert status == 200
        assert len(response["items"]) == 2
