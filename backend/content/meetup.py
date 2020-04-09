from guillotina import configure
from guillotina import schema
from guillotina import interfaces
from guillotina import content
from guillotina.fields.files import CloudFileField
from zope.interface import Interface


class ILink(Interface):
    platform = schema.Choice(values=("instagram", "youtube", "facebook"), required=True)
    url = schema.TextLine(required=True)


class IMeetup(interfaces.IItem):
    # user =
    title = schema.TextLine()
    description = schema.Text()
    img = CloudFileField(required=False)
    links = schema.List(value_type=schema.Object(schema=ILink))
    start = schema.Datetime(required=True)
    end = schema.Datetime(required=True)
    categories = schema.List(value_type=schema.TextLine())
    subcategories = schema.List(value_type=schema.TextLine())


@configure.contenttype(
    type_name="Meetup", schema=IMeetup, globally_addable=False,
)
class Meetup(content.Item):
    """
    Our Meetup type
    """
