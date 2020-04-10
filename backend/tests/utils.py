import json

USER_DATA = {"username": "masipcat", "email": "jordi@masip.cat", "password": "Patata"}


async def register_user(requester, **data):
    response, status = await requester(
        "POST", "/db/guillotina/@register", data=json.dumps(data)
    )
    assert status == 200
    return response


async def login_user(requester, username, password):
    response, status = await requester(
        "POST",
        "/db/guillotina/@login",
        data=json.dumps({"username": username, "password": password}),
    )
    assert status == 200
    token = response["token"]
    return f"Bearer {token}"
