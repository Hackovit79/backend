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
        await register_user(requester, **{**USER_DATA, "username": "user2"})

        response, status = await requester(
            "POST",
            "/db/guillotina/users/user2",
            data=json.dumps(
                {
                    "@type": "Meetup",
                    "title": "Concert directe",
                    "description": "Capitol 1 de molts",
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
                    "start": "2020-04-15T01:08:39+00:00",
                    "end": "2020-04-15T01:18:39+00:00",
                    "categories": ["gim"],
                    "subcategories": [],
                    "links": [{"platform": "youtube", "url": "www.youtube.com/live"}],
                    "img": {"data": "YWRmYXNkZmFzZGY="},
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
                    "title": "Gim capitol 2",
                    "description": "",
                    "start": arrow.utcnow().format("YYYY-MM-DD HH:mm:ss ZZ"),
                    "end": arrow.utcnow()
                    .shift(hours=1)
                    .format("YYYY-MM-DD HH:mm:ss ZZ"),
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
        assert {True, False, False} == {i["has_img"] for i in response["items"]}

        response, status = await requester(
            "GET",
            "/db/guillotina/@meetup-filter?start_date=2020-04-15T01:00:30Z&end_date=2020-04-15T05:00:30Z",
        )
        assert status == 200
        assert len(response["items"]) == 1

        response, status = await requester(
            "GET",
            "/db/guillotina/@meetup-filter?start_date=2020-04-11&end_date=2020-04-20&search=capitol",
        )
        assert status == 200
        assert len(response["items"]) == 2

        response, status = await requester(
            "GET",
            "/db/guillotina/@meetup-filter?start_date=2020-04-11&end_date=2020-04-20&search=cpitols",
        )
        assert status == 200
        assert len(response["items"]) == 2
