from collections import OrderedDict

from db.server import start_postgres
from db.plugins import Psycopg2Plugin
from db.tools import Psycopg2Tool

from settings import get_settings
import cherrypy


class Root(object):

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def index(self):
        base = cherrypy.request.base
        crud = OrderedDict([
            ('C', base + '/create/?name=test'),
            ('R', base + '/read/'),
            ('U', base + '/update/?name=test&newname=test_updated'),
            ('D', base + '/delete/?name=test_updated')
        ])
        return {'example_commands': crud}

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def create(self, name):
        cur = cherrypy.request.db.cursor()
        cur.execute('INSERT INTO testing (name) VALUES (%s);', (name,))
        raise cherrypy.HTTPRedirect('/read/')

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def read(self):
        cur = cherrypy.request.db.cursor()
        cur.execute('SELECT * from testing;')
        results = cur.fetchall()
        if results:
            return [dict(id=r[0], name=r[1]) for r in results]
        return []

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def update(self, name, newname):
        cur = cherrypy.request.db.cursor()
        cur.execute(
            'UPDATE testing SET name=%s WHERE name=%s;', (newname, name))
        raise cherrypy.HTTPRedirect('/read/')

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def delete(self, name):
        cur = cherrypy.request.db.cursor()
        cur.execute("DELETE FROM testing WHERE name=%s;", (name,))
        raise cherrypy.HTTPRedirect('/read/')


def create_app():
    dbsettings = get_settings().get('database')
    Psycopg2Plugin(cherrypy.engine, dbsettings).subscribe()
    cherrypy.tools.db = Psycopg2Tool()

    config = {
        '/': {
            'tools.db.on': True,
        }
    }
    cherrypy.tree.mount(Root(), '/', config)
    return cherrypy.tree


def run():
    try:
        # Starting the PostgreSQL Server
        pg_instance = None
        pg_instance = start_postgres()
        application = create_app()

        cherrypy.config.update({
            # 'server.socket_host': '0.0.0.0',
            'server.socket_port': 8000,
        })
        cherrypy.engine.signals.subscribe()
        cherrypy.engine.start()
        cherrypy.engine.block()
    finally:
        if pg_instance:
            pg_instance.destroy()


if __name__ == '__main__':
    run()
