import asyncio
import pytest


pytestmark = pytest.mark.asyncio


async def test_install(backend_requester):  # noqa
    async with backend_requester as requester:
        response, _ = await requester("GET", "/db/guillotina/@addons")
        assert "backend" in response["installed"]
