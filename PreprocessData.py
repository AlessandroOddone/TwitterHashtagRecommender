from os.path import expanduser
import csv
import string
from nltk import word_tokenize
from nltk.corpus import stopwords, treebank
from nltk import BigramTagger, UnigramTagger, AffixTagger


HASHTAGS_LIST = ['#dwts', '#glee', '#idol', '#xfactor', '#news', '#fashion', '#health', '#fail', '#jobs', '#business',
                 '#sales', '#economy', '#marketing', '#socialmedia', '#startup', '#edtech', '#education', '#teachers',
                 '#climate', '#solar', '#globalwarming', '#socialgood', '#cause', '#volunteer', '#4change']


STOPWORDS = set(stopwords.words("english"))
TAGS_TO_KEEP = ['NN', 'VB', 'JJ', 'RB']
FREQ_THRESHOLD = 5
FREQ_INTERVAL = 5000
FREQ_LIST = []


def write_file(data):
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "training.csv"
    #file_name = "validation.csv"
    tweets = data.get_tweets()
    hashtags = data.get_hashtags()
    rows = [[tweets[i], hashtags[i]] for i in range(0, len(tweets))]
    with open(home + path_to_file + file_name, 'wb') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)


#remove all the stopwords from a tweet
def tokenize_and_remove_stopwords(tweet):
    word_list = word_tokenize(tweet)
    words_to_keep = []
    for word in word_list:
        if not word.lower() in STOPWORDS and not len(word) < 3:
            words_to_keep.append(word)
    return ' '.join(words_to_keep)


#remove all the hashtags from a tweet
def remove_hashtags(tweet):
    word_list = tweet.split()
    words_to_keep = []
    for word in word_list:
        if not word.startswith('#'):
            words_to_keep.append(word)
        '''
        elif word not in HASHTAGS_LIST:
            words_to_keep.append(word[1:])
        '''
    return ' '.join(words_to_keep)


#remove html entities like &amp
def remove_html_entities(tweet):
    word_list = tweet.split()
    words_to_keep = []
    for word in word_list:
        if not word.startswith('&'):
            words_to_keep.append(word)
    return ' '.join(words_to_keep)


#remove user tags like @AlessandroOddone
def remove_user_tags(tweet):
    word_list = tweet.split()
    words_to_keep = []
    for word in word_list:
        if not word.startswith('@'):
            words_to_keep.append(word)
    return ' '.join(words_to_keep)


#delete punctuation, but not all non-alphabetic characters
def remove_punctuation_shallow(tweet):
    tweet.translate(string.maketrans("", ""), string.punctuation)


#filter out all symbols and punctuation except apostrophes
def filter_symbols(char):
    if ord(char) in range(65, 91) or ord(char) in range(97, 123) or char == ' ' or char == '\'':
        return char
    else:
        return ''


#remove all non-alphabetic characters
def remove_punctuation_deep(tweet):
    return filter(filter_symbols, tweet)


#remove all multiple spaces between characters
def remove_multiple_spaces(tweet):
    return ' '.join(tweet.split())


#return true if a word appears in at least FREQ_THRESHOLD tweets, false otherwise
def is_frequent(word, data, index):
    tweets = data.get_tweets()
    count = 0
    for i in range(index, FREQ_INTERVAL):
        tweet = tweets[i]
        for w in tweet:
            if word == w:
                count += 1
                break
        if count >= FREQ_THRESHOLD:
            return True
        if i >= (len(tweets) - 1):
            break
    return False


#return true if a word is frequent in the dataset, false otherwise
def is_frequent_word(word, data, index):
    if word in FREQ_LIST:
        return True
    elif is_frequent(word, data, index):
        FREQ_LIST.append(word)
        return True
    return False


#return true if the tag contains a tag in TAGS_TO_KEEP, false otherwise
def tag_to_keep(tag):
    for t in TAGS_TO_KEEP:
            if t in tag:
                return True
    return False


#read slang dictionary from file
def load_slang_dictionary():
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "slang.csv"
    with open(home + path_to_file + file_name, 'rb') as f:
        rows = []
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL):
            rows.append(row)
    return rows


#translate slang words contained in the tweet
def translate_slang(tweet):
    slang_dictionary = load_slang_dictionary()
    words_original = tweet.split()
    words_modified = []
    for word in words_original:
        temp = word
        for i in range(len(slang_dictionary)):
            if word == slang_dictionary[i][0]:
                temp = slang_dictionary[i][1]
                break
        words_modified.append(temp)
    return ' '.join(words_modified)


#keep only words in a tweet tagged as in TAGS_TO_KEEP or words that are frequent in the dataset
def pos_tag_filter(tweet, data, tagger):
    tagged_tweet = tagger.tag(word_tokenize(tweet))
    words_to_keep = []
    for i in range(len(tagged_tweet)):
        tagged_word = tagged_tweet[i]
        word = tagged_word[0]
        tag = tagged_word[1]
        if tag is not None:
            if tag_to_keep(tag):
                words_to_keep.append(word)
        elif is_frequent_word(word, data, i):
                words_to_keep.append(word.lower())
    return ' '.join(words_to_keep)


#filter out apostrophes
def apostrophe_filter(char):
    if not char == '\'':
        return char
    else:
        return ''


#remove apostrophes from a tweet
def remove_apostrophes(tweet):
    return filter(apostrophe_filter, tweet)


#return true if the tweet is empty, false otherwise
def is_empty(tweet):
    return tweet in ''


def process(data):
    processed_tweets = []
    t0 = AffixTagger(train=treebank.tagged_sents())
    t1 = UnigramTagger(train=treebank.tagged_sents(), backoff=t0)
    t2 = BigramTagger(train=treebank.tagged_sents(), backoff=t1)
    count = 0
    for tweet in data.get_tweets():
        count += 1
        print count
        tweet = remove_hashtags(tweet)
        tweet = remove_user_tags(tweet)
        tweet = remove_html_entities(tweet)
        tweet = remove_punctuation_deep(tweet)
        tweet = tokenize_and_remove_stopwords(tweet)
        tweet = remove_apostrophes(tweet)
        tweet = remove_multiple_spaces(tweet)
        tweet = translate_slang(tweet)
        tweet = pos_tag_filter(tweet, data, t2)
        if not is_empty(tweet):
            processed_tweets.append(tweet)
    data.set_tweets(processed_tweets)


class Dataset:
    tweets = []
    hashtags = []

    def __init__(self):
        home = expanduser("~")
        path_to_file = "/Desktop/NLP Project/"
        file_name = "training_original.csv"
        #file_name = "validation_original.csv"
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