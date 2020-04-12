from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import base64
import pytest

pytestmark = pytest.mark.asyncio


async def test_upload_download_avatar(backend_requester):
    async with backend_requester as requester:
        binary = b"X" * 1024

        await register_user(
            requester,
            **{**USER_DATA, "avatar": {"data": str(base64.b64encode(binary), "utf-8")}}
        )
        response, status = await requester("GET", "/db/guillotina/users/masipcat")
        assert status == 200

        response, status = await requester(
            "PATCH", "/db/guillotina/users/masipcat/@upload/avatar", data=binary
        )
        assert status == 200

        response, status = await requester(
            "GET", "/db/guillotina/users/masipcat/", authenticated=False,
        )
        assert status == 401

        response, status = await requester(
            "GET",
            "/db/guillotina/users/masipcat/@download/avatar",
            authenticated=False,
        )
        assert status == 200
        assert response == binary
