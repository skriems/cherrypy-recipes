import subprocess
from jaraco.postgres import PSQL
from jaraco.postgres import PostgresDatabase
from jaraco.postgres import PostgresServer

from textwrap import dedent
from settings import get_settings
from . import migrations


def start_postgres():
    dbsettings = get_settings().get('database')

    pg_instance = PostgresServer(port=dbsettings['port'])

    def sudo_psql(instance, args):
        argv = [
            PSQL,
            '--quiet',
            '-U', instance.superuser,
            '-h', instance.host,
            '-p', instance.port
        ] + args
        subprocess.check_call(argv)

    try:
        pg_instance.initdb()
        pg_instance.start()

        db_user = dbsettings['user']
        db_name = dbsettings['dbname']

        if db_name != 'postgres':
            sudo_psql(pg_instance, ['-c', 'CREATE ROLE %s SUPERUSER LOGIN' % db_user])

        db = PostgresDatabase(
            db_name,
            user=db_user,
            superuser=pg_instance.superuser,
            host=pg_instance.host,
            port=pg_instance.port,
        )

        # create the database
        db.create()

        # create the table if the user was changed
        if db_user != 'testuser':
            db.sql(dedent(
                """
                CREATE TABLE testing(
                    id integer PRIMARY KEY NOT NULL,
                    name text NOT NULL
                );
                GRANT SELECT, UPDATE, INSERT, DELETE ON testing TO %s;
                """ % dbsettings['user']))
        else:
            migrations.run()

    except Exception:
        pg_instance.destroy()
        raise
    return pg_instance
