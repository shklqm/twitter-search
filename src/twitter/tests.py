from django.test import TestCase, Client
import json

from twitter.constants import DEFAULT_USER_TWEETS


class SearchByHashTagTests(TestCase):
    def setUp(self):
        self.invalid_keyword = 'some_really_invalid_keyword'
        self.keyword = 'test'

        # bound to change in the future
        self.keyword_with_single_tweet = 'trucking_tst'

    def test_invalid_keyword(self):
        c = Client()
        response = c.get('/hashtags/{}'.format(self.invalid_keyword))
        content = response.content.decode()
        expected = {'message': 'No results for {}'.format(self.invalid_keyword)}

        result_content = json.loads(content)
        self.assertJSONEqual(json.dumps(result_content), json.dumps(expected))

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_default_tweet_number(self):
        c = Client()
        response = c.get('/hashtags/{}'.format(self.keyword))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), DEFAULT_USER_TWEETS)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_29_tweets(self):
        c = Client()
        response = c.get('/hashtags/{}?limit=29'.format(self.keyword))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 29)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_31_tweets(self):
        c = Client()
        response = c.get('/hashtags/{}?limit=31'.format(self.keyword))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 31)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_single_tweet(self):
        c = Client()
        response = c.get('/hashtags/{}'.format(self.keyword_with_single_tweet))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 1)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_single_tweet_with_limit(self):
        c = Client()
        response = c.get('/hashtags/{}?limit=100'.format(self.keyword_with_single_tweet))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 1)

        status_code = response.status_code
        self.assertEqual(status_code, 200)


class GetUserTweetsTests(TestCase):
    def setUp(self):
        self.invalid_user_name = 'some_invalid_user'
        self.username = 'twitter'

        # bound to change in the future
        self.username_with_no_tweets = 'asdfsdaf'

    def test_invalid_user(self):
        c = Client()
        response = c.get('/users/{}'.format(self.invalid_user_name))
        content = response.content.decode()
        expected = {'error': 'Invalid username'}

        result_content = json.loads(content)
        self.assertJSONEqual(json.dumps(result_content), json.dumps(expected))

        status_code = response.status_code
        self.assertEqual(status_code, 404)

    def test_default_tweet_number(self):
        c = Client()
        response = c.get('/users/{}'.format(self.username))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), DEFAULT_USER_TWEETS)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_29_tweets(self):
        c = Client()
        response = c.get('/users/{}?limit=29'.format(self.username))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 29)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_get_31_tweets(self):
        c = Client()
        response = c.get('/users/{}?limit=31'.format(self.username))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 31)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_user_has_no_tweets(self):
        c = Client()
        response = c.get('/users/{}?limit=31'.format(self.username_with_no_tweets))
        content = response.content.decode()

        result_content = json.loads(content)

        self.assertEqual(len(result_content), 0)

        status_code = response.status_code
        self.assertEqual(status_code, 200)
