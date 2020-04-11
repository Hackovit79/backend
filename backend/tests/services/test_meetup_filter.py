from backend.tests.utils import login_user
from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import arrow
import asyncio
import json
import pytest

pytestmark = pytest.mark.asyncio


async def test_meetup_filter(backend_requester):
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
                    "start": "2020-04-15T01:17:39+00:00",
                    "end": "2020-04-15T01:18:39+00:00",
                    "categories": ["gim"],
                    "subcategories": [],
                    "links": [{"platform": "youtube", "url": "www.youtube.com/live"}],
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
                    "title": "Gim2",
                    "description": "",
                    "start": arrow.utcnow().format(),
                    "end": arrow.utcnow().shift(hours=1).format(),
                    "categories": ["gim"],
                    "subcategories": [],
                    "links": [
                        {"platform": "instagram", "url": "www.instagram.com/live"}
                    ],
                }
            ),
        )
        assert status == 201

        # Wait until guillotina sends documents to ES
        await asyncio.sleep(2)

        response, status = await requester("GET", "/db/guillotina/@meetup-filter")
        assert status == 200
        assert len(response["items"]) == 3

        response, status = await requester(
            "GET",
            "/db/guillotina/@meetup-filter?user=masipcat&category=gim&start_date=2020-04-11&end_date=2020-04-20",
        )
        assert status == 200
        assert len(response["items"]) == 2

        response, status = await requester(
            "GET",
            "/db/guillotina/@meetup-filter?user=masipcat&category=gim&start_date=2020-04-11&end_date=2020-04-20&platform=instagram",
        )
        assert status == 200
        assert len(response["items"]) == 1

        response, status = await requester(
            "GET",
            "/db/guillotina/@meetup-filter?start_date=2020-04-11&end_date=2020-04-20",
        )
        assert status == 200
        assert len(response["items"]) == 3
