from backend.utils import json_response
from guillotina import configure
from guillotina import task_vars
from guillotina.component import get_utility
from guillotina.interfaces import IContainer
from guillotina_elasticsearch.interfaces import IElasticSearchUtility

import arrow


@configure.service(
    context=IContainer,
    method="GET",
    permission="guillotina.Public",
    name="@meetup-filter",
    allow_access=True,
)
async def meetup_filter(context, request):

    musts = [{"term": {"type_name": "Meetup"}}]
    shoulds = []
    el_query = {
        "query": {"bool": {"must": musts, "should": shoulds}},
        "aggs": {"categories": {"terms": {"field": "categories"}}},
        "sort": ["start"],
    }

    if request.query.get("user"):
        musts.append({"term": {"user": request.query.get("user")}})

    if request.query.get("category"):
        musts.append({"term": {"categories": request.query.get("category")}})

    if request.query.get("start_date") and request.query.get("end_date"):
        musts.append(
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
    elif request.query.get("start_date"):
        musts.append({"term": {"start": request.query.get("start_date")}})
    elif request.query.get("end_date"):
        musts.append({"term": {"end": request.query.get("end_date")}})
    else:
        # By default, we only return non-finished meetups
        musts.append({"range": {"end": {"gte": arrow.utcnow().isoformat()}}})

    if request.query.get("platform"):
        musts.append(
            {
                "nested": {
                    "path": "links",
                    "query": {
                        "bool": {
                            "must": {
                                "match": {
                                    "links.platform": request.query.get("platform")
                                }
                            }
                        }
                    },
                }
            }
        )

    if request.query.get("search"):
        shoulds.append(
            {"match": {"title": {"query": request.query.get("search"), "fuzziness": 2}}}
        )
        shoulds.append(
            {
                "match": {
                    "description": {
                        "query": request.query.get("search"),
                        "fuzziness": 2,
                    }
                }
            }
        )
        el_query["query"]["bool"]["minimum_should_match"] = 1

    es = get_utility(IElasticSearchUtility)
    resp = await es.search_raw(task_vars.container.get(), el_query, size=10)

    return json_response(200, resp)
