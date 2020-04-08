from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import json
import pytest


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('backend')
    else:
        settings['applications'] = ['backend']


testing.configure_with(base_settings_configurator)


class backend_Requester(ContainerRequesterAsyncContextManager):  # noqa

    async def __aenter__(self):
        await super().__aenter__()
        resp = await self.requester(
            'POST', '/db/guillotina/@addons',
            data=json.dumps({
                'id': 'backend'
            })
        )
        return self.requester


@pytest.fixture(scope='function')
async def backend_requester(guillotina):
    return backend_Requester(guillotina)
