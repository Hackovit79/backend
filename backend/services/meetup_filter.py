from backend.utils import json_response
from guillotina import configure
from guillotina import task_vars
from guillotina.component import get_utility
from guillotina.content import create_content_in_container
from guillotina.contrib.dbusers.content.users import User
from guillotina.event import notify
from guillotina.events import ObjectAddedEvent
from guillotina.interfaces import IContainer
from guillotina_elasticsearch.interfaces import IElasticSearchUtility


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.Public",
    name="@meetup-filter",
    allow_access=True,
)
async def meetup_filter(context, request):
    el_query = {"query": {"bool": {"must": []}}}
    if request.query.get("user"):
        el_query["query"]["bool"]["must"].append(
            {"term": {"user": request.query.get("user")}}
        )

    if request.query.get("category"):
        el_query["query"]["bool"]["must"].append(
            {"term": {"categories": request.query.get("category")}}
        )

    if request.query.get("start_date") and request.query.get("end_date"):
        el_query["query"]["bool"]["must"].append(
            {
                "range": {
                    "start": {
                        "gte": request.query.get("start_date"),
                        "lte": request.query.get("end_date"),
                        "relation": "within",
                    }
                }
            }
        )
    elif request.query.get("start_date") and request.query.get("end_date") is None:
        el_query["query"]["bool"]["must"].append(
            {"term": {"start": request.query.get("start_date")}}
        )

    if request.query.get("platform"):
        el_query["query"]["bool"]["must"].append(
            {"term": {"platform": request.query.get("platform")}}
        )

    es = get_utility(IElasticSearchUtility)
    resp = await es.search_raw(task_vars.container.get(), el_query, size=10,)
    return json_response(200, resp)
