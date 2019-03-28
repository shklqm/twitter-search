# Twitter-search

### How to run

Docker engine and docker-compose is required to run this properly. 


Inside the `docker` directory run the docker-compose up command

    docker-compose up --build -d

The `-d` argument can be omitted for not running it as a daemon. 

To view the latest logs run 

    docker-compose logs --tail=0 -f

This will create a Django application inside the docker container and it will run on `localhost:8004`


### Running sample tests

    docker exec -it twitter-search python manage.py test

### Features

**1. Get tweets by a hashtag.** Get the list of tweets with the given hashtag.

Optional parameters:
 
-`limit`: integer, specifies the number of tweets to retrieve, the default is 30

Example request:

    curl -H "Accept: application/json" -X GET http://localhost:8004/hashtags/python?limit=20
    
    
**2. Get user tweets.** Get the list of tweets that the user has on his feed. 

Optional parameters: 

-`limit`: integer, specifies the number of tweets to retrieve, the default is 30

Example request:

    curl -H "Accept: application/json" -X GET http://localhost:8004/users/twitter?limit=20


### How does it work

This application uses scrapping for getting data from Twitter. The idea is to paginate according to `limit` variable.

First the `position` variable is obtained. This serves as a next page id when requesting more tweets
.

In each request a blob response is returned from Twitter, which contains information of whether there is a next page and the tweets list in html format.

Then the `position` variable is updated, tweets list is parsed and returned.
