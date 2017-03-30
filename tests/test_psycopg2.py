from psycopg2_app import create_app

import pytest
import webtest


@pytest.fixture(scope='module')
def app():
    return webtest.TestApp(create_app())


class Testing(object):
    def test_create(self, app):
        resp = app.get('/create?name=test')
        assert resp.status == '201 Created'
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json['status'] == 'Created'

    def test_read(self, app):
        resp = app.get('/read/')
        assert resp.status == '200 OK'
        assert resp.headers['Content-Type'] == 'application/json'
        assert isinstance(resp.json, list), 'list of records'
        assert len(resp.json) == 1
        assert resp.json[0] == dict(id=1, name='test')

    def test_update(self, app):
        resp = app.get('/update?name=test&newname=testing')
        assert resp.status == '202 Accepted'
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json['status'] == 'Accepted'
        resp = app.get('/read')
        assert isinstance(resp.json, list), 'list of records'
        assert len(resp.json) == 1
        assert resp.json[0] == dict(id=1, name='testing')

    def test_delete(self, app):
        resp = app.get('/delete?name=testing')
        assert resp.status == '202 Accepted'
        assert resp.headers['Content-Type'] == 'application/json'
        resp = app.get('/read')
        assert isinstance(resp.json, list), 'list of records'
        assert len(resp.json) == 0
