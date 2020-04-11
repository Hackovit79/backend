from guillotina import configure
from guillotina import content
from guillotina import interfaces
from guillotina import schema
from guillotina.directives import index_field
from guillotina.fields.files import CloudFileField
from zope.interface import Interface


class ILink(Interface):
    index_field("platform", field_mapping={"type": "text"})
    platform = schema.Choice(values=("instagram", "youtube", "facebook"), required=True)
    url = schema.TextLine(required=True)


class IMeetup(interfaces.IItem):
    title = schema.TextLine()

    index_field("description", field_mapping={"type": "text"})
    description = schema.Text()

    img = CloudFileField(required=False)

    links = schema.List(value_type=schema.Object(schema=ILink))

    index_field("start", field_mapping={"type": "date"})
    start = schema.Datetime(required=True)

    index_field("end", field_mapping={"type": "date"})
    end = schema.Datetime(required=True)

    index_field("categories", field_mapping={"type": "keyword"})
    categories = schema.List(value_type=schema.TextLine())

    index_field("subcategories", field_mapping={"type": "keyword"})
    subcategories = schema.List(value_type=schema.TextLine())


@index_field.with_accessor(IMeetup, "user", field_mapping={"type": "keyword"})
def index_user(ob):
    return ob.__parent__.id


@index_field.with_accessor(IMeetup, "platform", field_mapping={"type": "keyword"})
def index_platform(ob):
    return [link["platform"] for link in ob.links or []]


@configure.contenttype(
    type_name="Meetup", schema=IMeetup, globally_addable=False,
)
class Meetup(content.Item):
    """
    Our Meetup type
    """
