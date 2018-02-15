# -*- coding: utf-8 -*-
import pytest


def _create_request(path, session, user='dummy'):
    from django.test import RequestFactory
    request = RequestFactory().get(path)
    request.session = session
    request.user = user
    return request


@pytest.fixture
def dashboard_request_with_no_session():
    return _create_request('/dashboard/', {})


@pytest.fixture
def dashboard_request_with_session():
    session = {'access_token_data': {'access_token': 'dummy_access_token',
                                             'access_token_secret': 'dummy_access_token_secret'}}
    return _create_request('/dashboard/', session)


@pytest.fixture
def dashboard_view():
    from .views import dashboard
    return dashboard


class TestTwitterMiddleWare:

    def _makeOne(self):
        from brochure.middleware import TwitterMiddleware
        return TwitterMiddleware(get_response=None)

    def test_if_session_has_not_access_token_then_redirect_top(self, dashboard_request_with_no_session, dashboard_view):
        middleware = self._makeOne()
        response = middleware.process_view(dashboard_request_with_no_session, dashboard_view, (), {})
        assert response.status_code == 302
        assert response.url == '/'

    def test_if_session_has_access_token_then_request_has_twitter_api(self,
                                                                      dashboard_request_with_session,
                                                                      dashboard_view):
        middleware = self._makeOne()
        response = middleware.process_view(dashboard_request_with_session, dashboard_view, (), {})
        assert response is None
        assert hasattr(dashboard_request_with_session, 'twitter_api')
