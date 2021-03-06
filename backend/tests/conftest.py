from pytest_docker_fixtures import images

images.configure(
    "elasticsearch",
    "docker.elastic.co/elasticsearch/elasticsearch-oss",
    "7.5.1",
    env={
        "xpack.security.enabled": None,  # unset
        "discovery.type": "single-node",
        "http.host": "0.0.0.0",
        "transport.host": "127.0.0.1",
    },
)

pytest_plugins = [
    "guillotina.tests.fixtures",
    "backend.tests.fixtures",
    "guillotina_elasticsearch.tests.fixtures",
    "pytest_docker_fixtures",
]
