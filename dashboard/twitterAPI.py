import wordcloud as WordCloud
import nltk
# nltk.download('wordnet')
# nltk.download('punkt')
import pickle
import regex as re
import warnings
import itertools
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from wordcloud import WordCloud, STOPWORDS
# import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
# stop_words = stopwords.words('english')
# nltk.download('stopwords')
# stop_words = stopwords.words('english')
warnings.filterwarnings("ignore")

import contractions as contractions
import tweepy
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)

#get trends from twitter
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

#get tweets from twitter
def getTweets(keyword):
    posts = api.search(q=keyword, lang="en", count = 3200,tweet_mode="extended")
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['tweets'])
    return df

# function to remove the elongated words
def remove_elongated(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)


# function to get the replace the short forms with dictionary forms
def load_slang():
    slangdict = dict()
    with open("C:\\Users\\M.FAIZAN\\tweetolytic\\tweetolytics\\text\\slangss.txt", 'rt') as f:
        for line in f:
            line = line.lower()
            spl = line.split('\t')
            slangdict[spl[0]] = spl[1][:-1]
    return slangdict


# data cleaning pipeline
def data_cleaning(tweet):
    tweet = re.sub("@[\w\d]+", " ", tweet)  # delete any references to other people
    tweet = re.sub("http:[\w\:\/\.]+", " ", tweet)  # replace url's
    tweet = re.sub('[^[A-Za-z]\s]', " ", tweet)  # replace non alphabets and non spaces
    tweet = re.sub('[^a-zA-Z]', " ", tweet)  # remoce non words (special characters)
    tweet = re.sub('[^\w\s]', " ", tweet)
    tweet = re.sub(r"\d*$", " ", tweet)  # numbers
    tweet = re.sub('(^\s+|\s+$)', " ", tweet)  # remove white spaces
    tweet = re.sub('RT', " ", tweet)
    tweet = tweet.lower()

    tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))
    return tweet


def data_tokenization(tweet):
    slang_words = load_slang()
    lem = WordNetLemmatizer()
    stemming = PorterStemmer()
    tokens = nltk.tokenize.word_tokenize(tweet)
    tokens = [token if len(token) > 1 else token.replace(token, "") for token in tokens]
    tokens = [token if token not in slang_words else slang_words[token] for token in tokens]
    # tokens = [stemming.stem(token) for token in tokens]
    tokens = [token for token in tokens if not token in stop_words]
    tokens = [lem.lemmatize(token) for token in tokens]
    tokens = [remove_elongated(token) for token in tokens]
    # tokens = [spell(token) for token in tokens
    return tokens


def rejoin_words(row):
    my_list = row['clean_tweets']
    joined_words = (" ".join(my_list))
    return joined_words


def call_functions(df):
    #basic_data_exploration(df.tweets)
    df["clean_tweets"] = df["tweets"].map(lambda x: data_cleaning(x))
    slang_words = load_slang()
    df["tweets"] = df["tweets"].apply(lambda x: contractions.fix(x))
    df["clean_tweets"] = df["clean_tweets"].map(lambda x: data_tokenization(x))
    df['final_clean_tweets'] = df.apply(rejoin_words, axis=1)
    wc = wordcloud(df['final_clean_tweets'].values)
    return wc


def wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, random_state=1,
                          background_color='white', max_words=100,colormap='Set2',
                          collocations=False, stopwords=STOPWORDS).generate(str(text))
    plt.figure(figsize=(30, 15),facecolor='k')
    plt.imshow(wordcloud,interpolation="nearest", aspect="auto")
    # No axis details
    plt.axis("off")
    save_results_to = 'C:\\Users\\M.FAIZAN\\tweetolytic\\tweetolytics\\static\\wordcloudimg\\'
    plt.savefig(save_results_to + 'image.png', bbox_inches='tight')
    # ppp = plt.show()
    fn="C:\\Users\\M.FAIZAN\\tweetolytic\\tweetolytics\\static\\wordcloudimg\\image.png"
    with open (fn,'rb') as f:
        data= f.read()
    return data


def main(keyword):
  dfs=getTweets(keyword)
  df = dfs
  pkl_filename = 'C:\\Users\\M.FAIZAN\\tweetolytic\\tweetolytics\\text\\Updated_Model.pkl'
  wc=call_functions(df)
  X_test = df['final_clean_tweets']

  # Load from file
  with open(pkl_filename, 'rb') as file:
      pickle_model = pickle.load(file)

  y_predict = pickle_model.predict(X_test)

  # print value of emotion
  total = y_predict.size
  angry = np.count_nonzero(y_predict == 0)
  happy = np.count_nonzero(y_predict == 1)
  negative = np.count_nonzero(y_predict == 2)
  neutral = np.count_nonzero(y_predict == 3)
  positive = np.count_nonzero(y_predict == 4)
  # print('Total = {}'.format(total))
  # print('angry = {}'.format(angry))
  # print('happy = {}'.format(happy))
  # print('negative = {}'.format(negative))
  # print('neutral = {}'.format(neutral))
  # print('positive = {}'.format(positive))

  return total, angry, happy, negative, neutral, positive,wc

if __name__ == "__main__":
    # pass
    main("psl6")
#     statistics()


