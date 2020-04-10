from backend.tests.utils import login_user
from backend.tests.utils import register_user
from backend.tests.utils import USER_DATA

import pytest

pytestmark = pytest.mark.asyncio


async def test_register_user(backend_requester):
    async with backend_requester as requester:
        await register_user(requester, **USER_DATA)
        await login_user(requester, USER_DATA["username"], USER_DATA["password"])
        response, status = await requester("GET", "/db/guillotina/users/masipcat",)
        assert status == 200
        assert {"username", "email", "avatar", "description"}.issubset(set(response))
