 #Importing the libraries
import pymongo
import time
import re
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

time.sleep(10) #seconds
### create connections to databases (check your mongosb and postgres in python notebooks (or luftdaten))
# Establish a connection to the MongoDB server
client1 = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database you want to use withing the MongoDB server
db = client1.twitter


#Add postgres credentials

DATABASE = 'tweet_db'
PORT = '5432'
USER = "tweet_postgres"
PASSWORD = "postgres"
HOST = 'postgresdb'

# # Clean your tweets
mentions_regex= '@[A-Za-z0-9]+'
url_regex='https?:\/\/\S+' #this will not catch all possible URLs
hashtag_regex= '#'
rt_regex= 'RT\s'

def clean_tweets(tweet):
    tweet = re.sub(mentions_regex, '', tweet)  #removes @mentions
    tweet = re.sub(hashtag_regex, '', tweet) #removes hashtag symbol
    tweet = re.sub(rt_regex, '', tweet) #removes RT to announce retweet
    tweet = re.sub(url_regex, '', tweet) #removes most URLs
    
    return tweet

# Create Sentiment Analyzer

analyzer = SentimentIntensityAnalyzer()

pg = create_engine('postgresql://postgres:postgres@postgresdb:5432/tweets', echo=True)

pg.execute('''
CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')

docs = db.tweets.find(limit=5)

for doc in docs:
    text= doc['text']
    text= clean_tweets(text)
    sentiment = analyzer.polarity_scores(text)
    score= sentiment['compound'] # placeholder value
    query = "INSERT INTO tweet VALUES (%s, %s);"
    pg.execute(query, (text, score))


