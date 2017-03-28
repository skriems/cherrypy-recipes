import os
from settings import get_settings
import psycopg2

CWD = os.path.dirname(os.path.abspath(__file__))


def run():
    dbsettings = get_settings().get('database')
    dbsettings.pop('minconn')
    dbsettings.pop('maxconn')

    migrations_folder = CWD
    migrations_scripts = [
        i for i in os.listdir(migrations_folder)
        if os.path.isdir(os.path.join(migrations_folder, i)) and
        i != '__pycache__'
    ]

    conn = psycopg2.connect(**dbsettings)
    conn.autocommit = True
    cur = conn.cursor()

    for m in migrations_scripts:
        script = os.path.join(migrations_folder, m, 'forward.sql')
        SQL = open(script).read()
        cur.execute(SQL)
