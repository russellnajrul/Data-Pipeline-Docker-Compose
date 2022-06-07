
import tweepy
import pymongo
import twitter_keys

client = tweepy.Client(bearer_token=twitter_keys.Bearer_Token)
client1 = pymongo.MongoClient(host="mongodb", port=27017)
db = client1.twitter
collection = db.tweets



bbc=client.get_user(username='BBCNews', user_fields=['name', 'id', 'created_at'])
user=bbc.data
print(bbc)

bbc_tweets = client.get_users_tweets(id=user.id, tweet_fields=['id', 'text', 'created_at'], max_results=100)
print(bbc_tweets.data)

dict(user)

print(f'the user with name {user.name} and ID {user.id} created their twitter account on {user.created_at}')
with open('bbc_tweets.txt',mode='a', encoding='utf8') as file:
    for tweet in bbc_tweets.data:
        print(f"The user {user.name} at {tweet.created_at} wrote: {tweet.text}\n")

        file.write('\n\n'+tweet.text)
    file.close()

for tweet in bbc_tweets.data:
    db.bbc_tweet.insert_one(tweet.data)




