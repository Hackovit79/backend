from guillotina import configure
from guillotina.api.service import Service
from guillotina.content import create_content_in_container
from guillotina.contrib.dbusers.content.users import IUserManager
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
class RegisterUser(Service):
    ALLOWED_FIELDS = ("username", "email", "name", "password")

    async def __call__(self):
        users_folder = await self.context.async_get("users")
        payload = await self.request.json()
        fields = {k: v for k, v in payload.items() if k in self.ALLOWED_FIELDS}
        user: User = await create_content_in_container(
            users_folder, "User", fields["username"], check_security=False, **fields
        )
        await notify(ObjectAddedEvent(user))
        return {"id": user.username}
