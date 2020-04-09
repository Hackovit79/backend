from guillotina.contrib.dbusers.content.users import User
from guillotina.contrib.dbusers.content.users import IUser
from guillotina import configure
from guillotina import schema
from guillotina.fields.files import CloudFileField


class ICustomUser(IUser):
    description = schema.Text()
    avatar = CloudFileField()


@configure.contenttype(
    type_name="User",
    schema=ICustomUser,
    add_permission="guillotina.AddUser",
    behaviors=["guillotina.behaviors.dublincore.IDublinCore"],
    globally_addable=False,
    allowed_types=["Meetup"],
)
class CustomUser(User):
    pass
