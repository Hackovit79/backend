from guillotina import testing
from guillotina_elasticsearch.tests.fixtures import elasticsearch
from guillotina_elasticsearch.tests.fixtures import ESRequester

import json
import pytest


def base_settings_configurator(settings):
    if "applications" in settings:
        settings["applications"].append("backend")
    else:
        settings["applications"] = ["backend"]

    if "guillotina_elasticsearch" not in settings["applications"]:
        settings["applications"].append("guillotina_elasticsearch")

    settings["elasticsearch"] = {
        "index_name_prefix": "guillotina-",
        "connection_settings": {
            "hosts": [
                "{}:{}".format(
                    getattr(elasticsearch, "host", "localhost"),
                    getattr(elasticsearch, "port", "9200"),
                )
            ],
            "sniffer_timeout": None,
        },
    }

    settings["load_utilities"]["catalog"] = {
        "provides": "guillotina_elasticsearch.interfaces.IElasticSearchUtility",  # noqa
        "factory": "guillotina_elasticsearch.utility.ElasticSearchUtility",
        "settings": {},
    }


testing.configure_with(base_settings_configurator)


class backend_Requester(ESRequester):  # noqa
    async def __aenter__(self):
        await super().__aenter__()
        resp = await self.requester(
            "POST", "/db/guillotina/@addons", data=json.dumps({"id": "backend"})
        )

        resp, status = await self.requester(
            "POST", "/db/guillotina/@addons", data=json.dumps({"id": "dbusers"})
        )
        assert status == 200

        return self.requester


@pytest.fixture(scope="function")
async def backend_requester(elasticsearch, guillotina, event_loop):
    return backend_Requester(guillotina, event_loop)
