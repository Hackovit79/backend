from backend.utils import json_response
from guillotina import configure
from guillotina import task_vars
from guillotina.component import get_utility
from guillotina.interfaces import IContainer
from guillotina_elasticsearch.interfaces import IElasticSearchUtility


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.Public",
    name="@top-categories",
    allow_access=True,
)
async def top_categories(context, request):
    es = get_utility(IElasticSearchUtility)
    resp = await es.search_raw(
        task_vars.container.get(),
        {"aggs": {"categories": {"terms": {"field": "categories"}}}},
        size=10,
    )
    return json_response(200, resp)
