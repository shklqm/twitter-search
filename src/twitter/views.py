import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views import View

from twitter.constants import SEARCH_URL, USER_URL, DEFAULT_SEARCH_TWEETS, DEFAULT_USER_TWEETS, USER_AGENT
from twitter.utils import get_tweet_streams


class SearchByHashTag(View):
    def get(self, request, keyword):
        """
        Get a list of tweets by a given keyword.

        :param request:
        :param keyword:
        :return list of tweets
        """

        try:
            url = SEARCH_URL.format(keyword=keyword)
            response = requests.get(url, headers={'User-Agent': USER_AGENT})
        except requests.exceptions.HTTPError as e:
            return JsonResponse(data={'error': 'HTTPError: {}'.format(e)})
        except requests.exceptions.ConnectionError as e:
            return JsonResponse(data={'error': 'ConnectionError: {}'.format(e)})
        except requests.exceptions.Timeout as e:
            return JsonResponse(data={'error': 'TimeOutError: {}'.format(e)})

        soup = BeautifulSoup(response.text, 'lxml')

        # handle the case when there are no results for the given keyword
        if soup.find("div", {"class": "SearchEmptyTimeline"}):
            return JsonResponse(data={'message': 'No results for {}'.format(keyword)})

        limit = int(request.GET.get('limit', DEFAULT_SEARCH_TWEETS))
        result = get_tweet_streams(soup, limit, keyword=keyword)[:limit]

        return JsonResponse(data=result, safe=False)


class GetUserTweets(View):
    def get(self, request, username):
        """
        Get the list of tweets that the user has on his feed.

        :param request:
        :param username:
        :return list of tweets
        """

        try:
            url = USER_URL.format(username=username)
            response = requests.get(url, headers={'User-Agent': USER_AGENT})
        except requests.exceptions.HTTPError as e:
            return JsonResponse(data={'error': 'HTTPError: {}'.format(e)})
        except requests.exceptions.ConnectionError as e:
            return JsonResponse(data={'error': 'ConnectionError: {}'.format(e)})
        except requests.exceptions.Timeout as e:
            return JsonResponse(data={'error': 'TimeOutError: {}'.format(e)})

        soup = BeautifulSoup(response.text, 'lxml')

        # handle the case when user does not exist
        if soup.find("div", {"class": "errorpage-topbar"}):
            return JsonResponse(data={'error': 'Invalid username'}, status=404)

        limit = int(request.GET.get('limit', DEFAULT_USER_TWEETS))
        result = get_tweet_streams(soup, limit, username=username, from_user=True)[:limit]

        return JsonResponse(data=result, safe=False)
