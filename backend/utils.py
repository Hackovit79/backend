from guillotina.response import Response

import json


def json_response(status, body):
    return Response(body=json.dumps(body).encode("utf-8"), status=status)
