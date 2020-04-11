from backend.content.user import ICustomUser
from guillotina import configure
from guillotina.api.files import DownloadFile


@configure.service(
    context=ICustomUser,
    method="GET",
    name="@download/{field_name}",
    permission="guillotina.Public",
    allow_access=True,
)
@configure.service(
    context=ICustomUser,
    method="GET",
    name="@download/{field_name}/{filename}",
    permission="guillotina.Public",
    allow_access=True,
)
class PublicDownloadFile(DownloadFile):
    pass
