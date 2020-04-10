from guillotina import configure
from guillotina.content import create_content_in_container
from guillotina.contrib.dbusers.content.users import User
from guillotina.event import notify
from guillotina.events import ObjectAddedEvent
from guillotina.interfaces import IContainer


@configure.service(
    context=IContainer,
    method="POST",
    permission="guillotina.Public",
    name="@register",
    allow_access=True,
)
async def register(context, request):
    ALLOWED_FIELDS = ("description", "username", "email", "name", "password")
    users_folder = await context.async_get("users")
    payload = await request.json()
    fields = {k: v for k, v in payload.items() if k in ALLOWED_FIELDS}
    user: User = await create_content_in_container(
        users_folder, "User", fields["username"], check_security=False, **fields
    )
    await notify(ObjectAddedEvent(user))
    return {"id": user.username}
