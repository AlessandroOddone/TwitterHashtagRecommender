# se diversi tweet sono identici --> eliminarli (SPAM)
#vedere come gestire don't isn't, etc...
#vedere se mettere tutto minuscolo oppure no
#lasciare solo nomi, verbi, avverbi e aggettivi e parole non taggate che compaiono tante volte
#tradurre slang: vedere come fare
from os.path import expanduser
import csv
import string


def write_file(data):
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "training.csv"
    tweets = data.get_tweets()
    hashtags = data.get_hashtags()
    rows = [[tweets[i], hashtags[i]] for i in range(0, len(tweets))]
    with open(home + path_to_file + file_name, 'wb') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)


#this function removes the hashtags from a tweet
def remove_hashtags(tweet):
    words_list = tweet.split()
    words_to_keep = []
    for word in words_list:
        if not word.startswith('#'):
            words_to_keep.append(word)
    return ' '.join(words_to_keep)


#remove html entities like &amp
def remove_html_entities(tweet):
    words_list = tweet.split()
    words_to_keep = []
    for word in words_list:
        if not word.startswith('&'):
            words_to_keep.append(word)
    return ' '.join(words_to_keep)


#remove user tags like @AlessandroOddone
def remove_user_tags(tweet):
    words_list = tweet.split()
    words_to_keep = []
    for word in words_list:
        if not word.startswith('@'):
            words_to_keep.append(word)
    return ' '.join(words_to_keep)


#delete punctuation, but not all non-alphabetic characters
def remove_punctuation_shallow(tweet):
    tweet.translate(string.maketrans("", ""), string.punctuation)


def only_ascii(char):
    if (ord(char) in range(65, 91)) or (ord(char) in range(97, 123)) or char == ' ':
        return char
    else:
        return ''


#remove all non-alphabetic characters
def remove_punctuation_deep(tweet):
    return filter(only_ascii, tweet)


#remove all multiple spaces between characters
def remove_multiple_spaces(tweet):
    return ' '.join(tweet.split())


#return true if the tweet is empty, false otherwise
def is_empty(tweet):
    return tweet in ''


def process(data):
    processed_tweets = []
    for tweet in data.get_tweets():
        tweet = remove_hashtags(tweet)
        tweet = remove_html_entities(tweet)
        tweet = remove_user_tags(tweet)
        tweet = remove_punctuation_deep(tweet)
        tweet = remove_multiple_spaces(tweet)
        if not is_empty(tweet):
            processed_tweets.append(tweet)
    data.set_tweets(processed_tweets)


class Dataset:
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

    def set_hashtags(self, hashtags):
        self.hashtags = hashtags


if __name__ == '__main__':
    dataset = Dataset()
    process(dataset)
    write_file(dataset)