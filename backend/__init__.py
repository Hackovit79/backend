from guillotina import configure


app_settings = {
    # provide custom application settings here...
    "applications": ["guillotina.contrib.dbusers", "guillotina.contrib.catalog.pg"]
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan("backend.services")
    configure.scan("backend.content")
    configure.scan("backend.install")
