import pytest
from db.server import start_postgres


@pytest.fixture(scope='session', autouse=True)
def pg_instance():
    instance = None
    try:
        instance = start_postgres()
        yield instance
    except Exception as err:
        pytest.skip("Postgres not available ({err})".format(**locals()))
    if instance:
        instance.destroy()
