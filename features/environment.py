from behave import fixture
from behave.fixture import use_fixture_by_tag
from pytest_localserver import http


class FileHost:

    def __init__(self):
        self._servers = []

    def host_file(self, content):
        server = http.ContentServer()
        server.start()
        server.serve_content(content)

        self._servers.append(server)

    def get_all_urls(self):
        return [s.url for s in self._servers]

    def close_all_servers(self):
        for server in self._servers:
            server.stop()

        self._servers = []


@fixture
def server_http(context, timeout=10):
    file_host = FileHost()

    context.file_host = file_host
    context.add_cleanup(file_host.close_all_servers)

    return file_host


fixture_registry = {
    "fixture.server.http": server_http
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
