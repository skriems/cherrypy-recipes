README
---

[CherryPy](http://www.cherrypy.org/) recipes for reference...

#### currently covered:
- CherryPy Plugins and Tools for Psycopg2 and SQLAlchemy

_for the Psycopg2 app a PostgreSQL Server is started via [jaraco.postgres](https://github.com/jaraco/jaraco.postgres)_


## Setup

1. `pip install -r requirements.txt`
2. run the Psycopg2 example via `python psycopg2_app.py`
3. run the SQLAlchemy example via `python sqlalchemy_app.py`

Note: Since the SQLAlchemy Plugin is not yet using the PostgreSQL Server, you need to initialize the db via `python db/init_testdb.py` first.

## Credits

the SQLAlchemy Plugin and Tool was originally taken from [here](https://bitbucket.org/Lawouach/cherrypy-recipes/) and crafted by [Sylvain Hellegouarch](https://github.com/Lawouach)
