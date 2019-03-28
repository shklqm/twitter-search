import json

import requests
from bs4 import BeautifulSoup

from twitter.constants import USER_MORE_URL, SEARCH_MORE_URL, USER_AGENT


def get_tweet_account_info(tweet):
    stream_header = tweet.find("div", {"class": "stream-item-header"})
    account_group = stream_header.find("a", {
        "class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})
    name = account_group.find("strong", {"class": "fullname show-popup-with-id u-textTruncate"})
    posted_date = stream_header.find("a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})

    return {
        'account': {
            'fullname': name.text,
            'href': account_group["href"],
            'id': account_group["data-user-id"]
        },
        'date': posted_date['title']
    }


def get_tweet_footer_info(tweet):
    stream_footer = tweet.find("div", {"class": "stream-item-footer"})

    reply_group = stream_footer.find("div", {"class": "ProfileTweet-action ProfileTweet-action--reply"})
    reply_count = reply_group.find("span", {"class": "ProfileTweet-actionCount"})

    retweet_group = stream_footer.find("div", {
        "class": "ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt"})
    retweet_count = retweet_group.find("span", {"class": "ProfileTweet-actionCount"})

    favorite_group = stream_footer.find("div",
                                        {"class": "ProfileTweet-action ProfileTweet-action--favorite js-toggleState"})
    favorite_count = favorite_group.find("span", {"class": "ProfileTweet-actionCount"})

    # strip unnecessary spaces
    reply_count = reply_count.text.strip()
    retweet_count = retweet_count.text.strip()
    favorite_count = favorite_count.text.strip()

    return {
        'replies': int(reply_count) if reply_count else 0,
        'retweets': int(retweet_count) if retweet_count else 0,
        'likes': int(favorite_count) if favorite_count else 0,
    }


def get_tweet_text_and_hashtags(tweet, from_user=False):
    tweet_text = tweet.find("p", {"class": "TweetTextSize js-tweet-text tweet-text"})
    if from_user:
        tweet_text = tweet.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})

    hashtags = tweet_text.find_all("a", {"class": "twitter-hashtag pretty-link js-nav"})
    hashtag_list = [hashtag.text for hashtag in hashtags]

    return {
        'hashtags': hashtag_list,
        'text': tweet_text.text
    }


def parse_tweets(soup, from_user=False):
    parsed_tweets = []
    tweet_group = soup.find_all("li", {"data-item-type": "tweet"})

    if soup is not None:
        # parse each tweet and add it to parsed_tweets list
        for tweet in tweet_group:
            try:
                parsed_tweets.append({
                    **get_tweet_text_and_hashtags(tweet, from_user),
                    **get_tweet_account_info(tweet),
                    **get_tweet_footer_info(tweet)
                })
            except AttributeError:
                continue

    return parsed_tweets


def get_tweet_streams(soup, limit, keyword=None, username=None, from_user=False):
    # parse first page blob response
    all_tweets = parse_tweets(soup, from_user)

    # get the next position id. Used to fetch next page of tweets
    position = soup.find("div", {"class": "stream-container"})["data-min-position"]

    # iterate until number of tweets has reached the limit or until there no more tweets to load
    while len(all_tweets) < limit:
        next_url = SEARCH_MORE_URL.format(position=position, keyword=keyword)
        if from_user:
            next_url = USER_MORE_URL.format(username=username, position=position)

        try:
            response = requests.get(next_url, headers={'User-Agent': USER_AGENT})
        except requests.exceptions.HTTPError:
            break
        except requests.exceptions.ConnectionError:
            break
        except requests.exceptions.Timeout:
            break

        blob_response = json.loads(response.text)

        # check whether there are more tweets to load
        if not blob_response["has_more_items"]:
            break

        position = blob_response["min_position"]
        soup = BeautifulSoup(blob_response["items_html"], 'lxml')

        # parse the blob response and add it to all_tweets
        for tweet in parse_tweets(soup, from_user):
            all_tweets.append(tweet)

    return all_tweets
