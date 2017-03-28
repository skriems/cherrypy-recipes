# -*- coding: utf-8 -*-
from collections import OrderedDict

from db.plugins import SAEnginePlugin
from db.tools import SATool
from db.sa_models import Entry

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
            ('D', base + '/delete/?id=1')
        ])
        return {'examples_commands': crud}

    @cherrypy.expose
    def create(self, name):
        db = cherrypy.request.db
        user = Entry(name=name)
        db.add(user)
        raise cherrypy.HTTPRedirect('/read')

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def read(self):
        db = cherrypy.request.db

        query = db.query(Entry).order_by(Entry.id)
        entries = {}
        for entry in query:
            entries[entry.id] = entry.name

        return {'entries': entries}

    @cherrypy.expose
    def update(self, name, newname):
        db = cherrypy.request.db
        user = db.query(Entry).filter(Entry.name == name).first()
        user.name = newname
        raise cherrypy.HTTPRedirect('/read')

    @cherrypy.expose
    def delete(self, id):
        db = cherrypy.request.db
        entry = db.query(Entry).filter(Entry.id == id).first()
        db.delete(entry)
        raise cherrypy.HTTPRedirect('/read')


def create_app():
    SAEnginePlugin(cherrypy.engine, 'sqlite:///db/test.db').subscribe()
    cherrypy.tools.db = SATool()

    config = {
        '/': {
            'tools.db.on': True,
        }
    }
    cherrypy.tree.mount(Root(), '/', config)
    return cherrypy.tree


def run():
    application = create_app()
    cherrypy.config.update({
            # 'server.socket_host': '0.0.0.0',
            'server.socket_port': 8000,
        })
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    run()
else:  # WSGI
    app = create_app()
