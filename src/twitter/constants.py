DEFAULT_SEARCH_TWEETS = 30
DEFAULT_USER_TWEETS = 30

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'

SEARCH_URL = 'https://twitter.com/search?f=tweets&vertical=default&q={keyword}'
SEARCH_MORE_URL = 'https://twitter.com/i/search/timeline?f=tweets&vertical=' \
             'default&include_available_features=1&include_entities=1&' \
             'reset_error_state=false&src=typd&max_position={position}&q={keyword}'

USER_URL = 'https://twitter.com/{username}'
USER_MORE_URL = 'https://twitter.com/i/profiles/show/{username}/timeline/tweets?' \
                  'include_available_features=1&include_entities=1&' \
                  'max_position={position}&reset_error_state=false'
