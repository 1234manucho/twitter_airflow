import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs


def run_twitter_etl():
    # Twitter API credentials
    access_key = "DcOhMlarfdwV1XLsVmWF7iFeH"
    access_secret = "PoWwB6KATVGAiLtv15LfDCLFlGKltNSvav0rnMtBHYn1Scl0zq "
    consumer_key = "1781701876813029376-nrTvg1sM48F3ybvNYnr3Uz3VY1lkbd"
    consumer_secret = "OgJFNRJV3uiW4tZqKWEXdMJIkf5vyhE4eoSSrnfNDT0f8  "

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(access_key, access_secret)
    auth.set_access_token(consumer_key, consumer_secret)

    # Create API object
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name="@DSEAfrica", 
                               #200 is the max number of tweets you can get
                               count=200, 
                                include_rts=False,
                                #use extended mode to get full text of tweets
                               tweet_mode="extended"
                               #otherwise, you will get truncated text
                               )
    # Create a list to store the tweets
    tweets_list = []
    for tweet in tweets:
        text = tweet.__json['full_text']
        
        refined_tweet = {"user": tweet.user.screen_name,
                         'text': text,
                         'favorite_count': tweet.favorite_count,
                         'retweet_count': tweet.retweet_count,
                         'created_at': tweet.created_at,}
        tweets_list.append(refined_tweet)
        
    df = pd.DataFrame(tweets_list)
    df.to_csv("s3://chills-airflow-bucket/elonmusk_twitter_data.csv")