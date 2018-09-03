import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import csv


# Step 1 - Authenticate

def init():
    consumer_key = 'Ru76PhPKLnc4NxJtPDCO7cQWI'
    consumer_secret = 'llAP3oO3tBKqPPVwmZmQlhtTUwWbMNcGcKybKFPetHsmVCTmTF'

    access_token = '1470639566-ZHXE2QnIs8oR2yjCQ49w3FXitYLpp7DpOS4YJ8q'
    access_token_secret = 'amHSLVzqoVcrAJqwVPP9e2nWsHm15D0wEH41KrX0IWnhC'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    global api
    api = tweepy.API(auth)


# Get tweets from user_timeline and save in csv file

def getTweetsfromTimeLine(screen_name, count=None, includeRT=None):
    # //call tweeter API

    new_tweets = api.user_timeline(screen_name=screen_name, count=count, tweet_mode="extended", include_rts=includeRT)
    tweet_full_text = ([tweet.full_text for tweet in new_tweets])
    source = ([tweet.source for tweet in new_tweets])
    tweet_id = ([[tweet.id] for tweet in new_tweets])
    date = ([tweet.created_at for tweet in new_tweets])
    likes = ([tweet.favorite_count for tweet in new_tweets])
    RTs = ([tweet.retweet_count for tweet in new_tweets])
    polarity = []
    for tweet in tweet_full_text:
        temp = checkpolarity(tweet)
        polarity.append(temp)

    # Changing to pandas datastructure and ouptu to csv file
    data_output = {'Id': tweet_id,
                   'Tweet': tweet_full_text,
                   'Sentiment': polarity,
                   'Date': date,
                   'Source': source,
                   'Likes': likes,
                   'RTs': RTs

                   }
    df = pd.DataFrame(data_output, columns=['Id', 'Tweet', 'Sentiment', 'Date', 'Source', 'Likes', 'RTs'])
    df.to_csv('%s_tweets.csv' % screen_name)


# Search tweets for candidates and perform sentiment analysis and save each in csv file
def getTweetsFromSearchAPI(q, date_from, date_to, lang=None, count=None):
    for candidate_name in candidate_names:
        public_tweets = api.search(q, count=count, since=date_from, until=date_to, lang=lang, tweet_mode='extended')

        tweet_full_text_search = ([tweet.full_text for tweet in public_tweets])
        polarity = []
        for tweet in tweet_full_text_search:
            temp = checkpolarity(tweet)
            polarity.append(temp)

        search_data_output = {
                'Tweet': tweet_full_text_search,
                'Sentiment': polarity,

            }
        df = pd.DataFrame(search_data_output, columns=['Tweet', 'Sentiment'])
        df.to_csv('%s_tweets.csv' % candidate_name)


def checkpolarity(new_tweets):
    # for tweet in new_tweets:
    analysis = TextBlob(new_tweets)
    return analysis.polarity


def checksentencePolarity(new_tweets):
    analysis = TextBlob(new_tweets)
    print(analysis.polarity)


if __name__ == "__main__":
    # //Get twitter api
    init()

    # //Choose criteria for analysis and get ouput to csv file
    candidate_names = ['Trump']
    topic = ['']
    date_from = "2018-8-29"
    date_to = "2018-9-2"
    lang = "en"
    q = [candidate_names, topic]
    getTweetsFromSearchAPI(q, date_from, date_to, lang, count=1000)

    # //Get tweets from user timeline
    # //TODO THROW EXCEPTION IF PAGE DOESNT EXIST
    # getTweetsfromTimeLine(screen_name='realdonaldtrump', includeRT=False)

    # checksentencePolarity('Today I went to Barbeque Nation and the Food was very good')
