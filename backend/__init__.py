from guillotina import configure

app_settings = {
    # provide custom application settings here...
    "applications": [
        "guillotina.contrib.dbusers",
        # "guillotina.contrib.catalog.pg",
        "guillotina_elasticsearch",
    ],
    "elasticsearch": {
        "index_name_prefix": "guillotina-",
        "connection_settings": {
            "hosts": ["elasticsearch:9200"],
            "sniffer_timeout": 0.5,
            "sniff_on_start": True,
        },
        "security_query_builder": "guillotina_elasticsearch.queries.build_security_query",
    },
    "logging": {
        "version": 1,
        "formatters": {
            "brief": {"format": "%(message)s"},
            "default": {
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "brief",
                "level": "INFO",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "uvicorn": {"level": "INFO", "handlers": ["console"], "propagate": 0},
            "backend": {"level": "INFO", "handlers": ["console"], "propagate": 0},
            "guillotina": {"level": "DEBUG", "handlers": ["console"], "propagate": 1},
            "guillotina_elasticsearch": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": 1,
            },
            "guillotina_evolution": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": 1,
            },
        },
    },
}


def includeme(root):
    """
    custom application initialization here
    """
    configure.scan("backend.services")
    configure.scan("backend.content")
    configure.scan("backend.install")
