from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import pytest

pytestmark = pytest.mark.asyncio


async def test_upload_download_avatar(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **USER_DATA)
        response, status = await requester("GET", "/db/guillotina/users/masipcat")
        assert status == 200

        binary = b"X" * 1024

        response, status = await requester(
            "PATCH", "/db/guillotina/users/masipcat/@upload/avatar", data=binary
        )
        assert status == 200

        response, status = await requester("GET", "/db/guillotina/users/masipcat")
        assert status == 200
        filename = response["avatar"]["filename"]

        response, status = await requester(
            "GET", "/db/guillotina/users/masipcat/", authenticated=False,
        )
        assert status == 401

        response, status = await requester(
            "GET",
            f"/db/guillotina/users/masipcat/@download/avatar/{filename}",
            authenticated=False,
        )
        assert status == 200
        assert response == binary
