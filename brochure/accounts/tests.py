from django.test import TestCase, RequestFactory
from brochure.middleware import TwitterMiddleware
from .views import dashboard


class TwitterMiddleWareTest(TestCase):
    def setUp(self):
        self.middleware = TwitterMiddleware(get_response=None)
        self.factory = RequestFactory()

    def test_if_session_has_not_access_token_then_redirect_top(self):
        request = self.factory.get('/dashboard/')
        request.session = {}
        request.user = 'user'
        response = self.middleware.process_view(request, dashboard, (), {})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_if_session_has_access_token_then_request_has_twitter_api(self):
        request = self.factory.get('/dashboard/')
        request.session = {'access_token_data': {'access_token': 'dummy_access_token',
                                                 'access_token_secret': 'dummy_access_token_secret'}}
        request.user = 'user'
        response = self.middleware.process_view(request, dashboard, (), {})
        self.assertIsNone(response)
        self.assertTrue(hasattr(request, 'twitter_api'))
