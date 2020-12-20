import tweepy
# from twitter import *
consumerKey = "WjGKiCCQGJNnVVkzO2JKwqyWY"
consumerSecret = "KVnljXNKG7SJe8kFDrtwKQPvbWbXMP8W8LxZyaMVsAmKyezRde"
accessToken = "871078610936840192-qjwYEQ07OkAoNaANvcLiPQqInUpXhlG"
accessTokenSecret = "gxXWr8ojbYs0ZonCzszz5V2TC5qZREtc2rhLbp8NdKZ9i"

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)
def twitterTrends():
    trends=api.trends_place(2211096)
    a = trends[0]
    b = (a['trends'])
    name = []
    url = []
    for i in b[:10]:
        n = (i['name'])
        # print(n)
        name.append(n)

        u = (i['url'])
        # print(u)
        url.append(u)
    toptrends = tuple(name)
    urls = tuple(url)
    return toptrends

# t=Twitter()
twitterTrends()