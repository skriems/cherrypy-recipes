from copy import deepcopy

DEFAULTS = {
    'database': {
        'user': 'testuser',  # also change in migrations
        'password': 'test',
        'host': 'localhost',
        'port': 54321,
        'dbname': 'testdb',
        'minconn': 1,
        'maxconn': 5,
    }
}


def get_settings():
    return deepcopy(DEFAULTS)
