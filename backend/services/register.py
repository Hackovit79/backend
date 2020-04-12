from guillotina import configure
from guillotina import error_reasons
from guillotina.component import query_multi_adapter
from guillotina.content import create_content_in_container
from guillotina.contrib.dbusers.content.users import User
from guillotina.event import notify
from guillotina.events import ObjectAddedEvent
from guillotina.interfaces import IContainer
from guillotina.interfaces import IResourceDeserializeFromJson
from guillotina.response import ErrorResponse


@configure.service(
    context=IContainer,
    method="POST",
    permission="guillotina.Public",
    name="@register",
    allow_access=True,
)
async def register(context, request):
    users_folder = await context.async_get("users")
    data = await request.json()
    user: User = await create_content_in_container(
        users_folder, "User", data["username"], check_security=False,
    )

    deserializer = query_multi_adapter((user, request), IResourceDeserializeFromJson)
    if deserializer is None:
        return ErrorResponse(
            "DeserializationError",
            "Cannot deserialize type {}".format(user.type_name),
            status=412,
            reason=error_reasons.DESERIALIZATION_FAILED,
        )
    await deserializer(data, validate_all=True, create=True)

    await notify(ObjectAddedEvent(user))
    return {"id": user.username}
