from cherrypy.process import plugins

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from psycopg2.pool import ThreadedConnectionPool


class Psycopg2Plugin(plugins.SimplePlugin):
    def __init__(self, bus, settings):
        super(Psycopg2Plugin, self).__init__(bus)
        self.pool = ThreadedConnectionPool(**settings)
        self.bus.log('Started DB Connection Pool with %s/%s (min/max)'
                     ' connections.' % (settings['minconn'],
                                        settings['maxconn'])
                     )
        self.connection = None
        self.bus.subscribe('bind-connection', self.bind)
        self.bus.subscribe('commit-connection', self.commit)

    def stop(self):
        self.bus.log('Stopping DB Connection Pool')
        self.bus.unsubscribe('bind-connection', self.bind)
        self.bus.unsubscribe('commit-connection', self.commit)

    def bind(self):
        if not self.connection:
            self.connection = self.pool.getconn()
        return self.connection

    def commit(self):
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        finally:
            self.pool.putconn(self.connection)
            self.connection = None


class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus, connection_string=None):
        """
        The plugin is registered to the CherryPy engine and therefore
        is part of the bus (the engine *is* a bus) registery.

        We use this plugin to create the SA engine. At the same time,
        when the plugin starts we create the tables into the database
        using the mapped class of the global metadata.
        """
        plugins.SimplePlugin.__init__(self, bus)
        self.bus.log('Starting up DB access')
        self.sa_engine = None
        self.connection_string = connection_string
        self.sa_engine = create_engine(self.connection_string, echo=False)
        self.session = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))
        self.bus.subscribe("bind-session", self.bind)
        self.bus.subscribe("commit-session", self.commit)

    def stop(self):
        self.bus.log('Stopping down DB access')
        self.bus.unsubscribe("bind-session", self.bind)
        self.bus.unsubscribe("commit-session", self.commit)
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self):
        """
        Whenever this plugin receives the 'bind-session' command, it applies
        this method and to bind the current session to the engine.

        It then returns the session to the caller.
        """
        self.session.configure(bind=self.sa_engine)
        return self.session

    def commit(self):
        """
        Commits the current transaction or rollbacks if an error occurs.

        In all cases, the current session is unbound and therefore
        not usable any longer.
        """
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.remove()
