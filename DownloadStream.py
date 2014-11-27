from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import langid
from datetime import date
from os.path import expanduser
import csv
import Auth


HASHTAGS_LIST = ['#dwts', '#glee', '#idol', '#xfactor', '#news', '#fashion', '#health', '#fail', '#jobs', '#business',
                 '#sales', '#economy', '#marketing', '#socialmedia', '#startup', '#edtech', '#education', '#teachers',
                 '#climate', '#solar', '#globalwarming', '#socialgood', '#cause', '#volunteer', '#4change']


def is_retweet(status):
    if status.text.strip().find("RT") == 0:
        return True
    return False


def is_spam(status):
    text = status.text.strip()
    if ("http://" or "https://") in text or status.entities['urls']:
        return True
    user = status.user
    created_at = str(user.created_at)
    year = int(created_at[0:4])
    month = int(created_at[5:7])
    day = int(created_at[8:10])
    creation_date = date(year, month, day)
    today = date.today()
    if (today - creation_date).days < 100:
        return True
    return False


def is_english(status):
    if langid.classify(status.text.strip())[0] == 'en':
        return True
    return False


def add_to_database(status, hashtags):
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "new_tweets.csv"
    text = ' '.join(status.text.replace('\n', ' ').split()).encode('utf-8')
    rows = []
    for hashtag in hashtags:
        for h in HASHTAGS_LIST:
            if r'#' + hashtag.lower() == h.lower():
                rows.append([text, str(hashtag).lower()])
                break
    with open(home + path_to_file + file_name, 'ab') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)


class Listener(StreamListener):
    def on_status(self, status):
        hashtags = [hashtag['text'] for hashtag in status.entities['hashtags']]
        if hashtags and is_english(status) and not is_retweet(status) and not is_spam(status):
            print ("--------------------------------------")
            print ("**TWEET**: " + status.text.strip() + "\n" + "**HASHTAGS**: " + ', '.join(hashtags))
            add_to_database(status, hashtags)

    def on_error(self, status):
        print status


if __name__ == '__main__':
    COUNT = 0
    auth = OAuthHandler(Auth.CONSUMER_KEY, Auth.CONSUMER_SECRET)
    auth.set_access_token(Auth.ACCESS_TOKEN, Auth.ACCESS_TOKEN_SECRET)
    stream = Stream(auth, Listener())
    stream.filter(track=[','.join(HASHTAGS_LIST[i] for i in range(0, len(HASHTAGS_LIST)))])






