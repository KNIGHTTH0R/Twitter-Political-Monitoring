import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''

import tweepy
import csv
import pandas as pd

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#credentials
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#Adapted from https://gist.github.com/vickyqian/f70e9ab3910c7c290d9d715491cde44c
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

# Get user location
def get_user_loc(user):
    uloc = user.location
    return uloc

# Scrape tweets by hashtag
def get_tweets_htg(hashtag):
    filename = "{}.csv".format(hashtag)

    # Open/Create a file to append data
    csvFile = open(filename, 'a')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)
    for tweet in tweepy.Cursor(api.search,q=hashtag,count=20,
                              lang="en",
                              since="2018-12-19").items():
        csvWriter.writerow([get_user_loc(tweet.user), tweet.geo, tweet.place, tweet.coordinates, tweet.created_at, tweet.text.encode('utf-8')])
    return filename

# Scrape tweets by keyword
def get_tweets_kwd(keyword):
    filename = "{}.csv".format(keyword)

    # Open/Create a file to append data
    csvFile = open(filename, 'a')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)
    for tweet in tweepy.Cursor(api.search,q=keyword,count=20,
                              lang="en",
                              since="2018-01-01").items():
        csvWriter.writerow([get_user_loc(tweet.user), tweet.geo, tweet.place, tweet.coordinates, tweet.created_at, tweet.text.encode('utf-8')])
    return filename

# adapted from https://cloud.google.com/natural-language/docs/sentiment-tutorial
#analyzing_document_sentiment

def analyze(text):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()
    score_list = []
    # for each line, append the sentiment score and magnitude to the list
    with open(text) as review:
        for cnt, line in enumerate(review):
            document = types.Document(
                content=line,
                type=enums.Document.Type.PLAIN_TEXT)
            annotations = client.analyze_sentiment(document=document)
            score = annotations.document_sentiment.score
            score_list.append(annotations.document_sentiment.score)
            magnitude = annotations.document_sentiment.magnitude
            print('Result {}: score of {} with magnitude of {}'.format(cnt + 1,
                score, magnitude))
        return score_list

if __name__ == '__main__':
    qType = input("H for Hashtag search, K for keyword search: ")
    if qType == "H":
        hashtag = input("Hashtag: ")
        file = get_tweets_htg(hashtag)
    if qType == "K":
        keyword = input("Keyword: ")
        file = get_tweets_kwd(keyword)
        score_a = analyze(file)
