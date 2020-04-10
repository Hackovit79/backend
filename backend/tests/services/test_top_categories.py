from backend.tests.utils import login_user
from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import arrow
import asyncio
import json
import pytest

pytestmark = pytest.mark.asyncio


async def test_top_categories(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **USER_DATA)
        await login_user(requester, USER_DATA["username"], USER_DATA["password"])

        response, status = await requester(
            "POST",
            "/db/guillotina/users/masipcat",
            data=json.dumps(
                {
                    "@type": "Meetup",
                    "title": "Concert directe",
                    "description": "",
                    "start": arrow.utcnow().format(),
                    "end": arrow.utcnow().shift(hours=1).format(),
                    "categories": ["musica"],
                    "subcategories": ["rock"],
                }
            ),
        )
        assert status == 201

        response, status = await requester(
            "POST",
            "/db/guillotina/users/masipcat",
            data=json.dumps(
                {
                    "@type": "Meetup",
                    "title": "Gim",
                    "description": "",
                    "start": arrow.utcnow().format(),
                    "end": arrow.utcnow().shift(hours=1).format(),
                    "categories": ["gim"],
                    "subcategories": [],
                }
            ),
        )
        assert status == 201

        # Wait until guillotina sends documents to ES
        await asyncio.sleep(2)

        response, status = await requester("GET", "/db/guillotina/@top-categories")
        assert status == 200
