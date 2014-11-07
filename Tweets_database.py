__author__ = 'alessandro'

from os.path import expanduser
import csv

class Tweets_database:
    tweets = []
    hashtags = []

    def __init__(self):
        home = expanduser("~")
        path_to_file = "/Desktop/NLP Project/"
        file_name = "tweets.csv"
        with open(home + path_to_file + file_name, 'rb') as f:
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL):
            self.tweets.append(row[0])
            self.hashtags.append(row[1])

    def get_tweets(self):
        return self.tweets

    def get_hashtags(self):
        return self.hashtags

    def set_tweets(self, tweets):
        self.tweets = tweets

    def set_hashtag(self, hashtags):
        self.hashtags = hashtags