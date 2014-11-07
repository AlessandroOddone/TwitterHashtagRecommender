import nltk
from sklearn import cross_validation
from collections import defaultdict
from os.path import expanduser
import csv


def read_file():
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "training.csv"
    with open(home + path_to_file + file_name, 'rb') as f:
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL):
            tweets_read.append(row[0])
            hashtags_read.append(row[1])


def unigrams(tweet):
    features = defaultdict(list)
    words = tweet.split()
    for w in words:
            features[w] = True
    return features


def feature_extractor(tweet):
    return unigrams(tweet)


def features_from_tweets(tweets, hashtags):
    feature_labels = []
    for i in range(0, len(tweets)):
        features = feature_extractor(tweets[i])
        feature_labels.append((features, hashtags[i]))
    return feature_labels


def train_model(tweets, hashtags):
    train_set = features_from_tweets(tweets, hashtags)
    cv = cross_validation.KFold(len(train_set), n_folds=10)
    sum_accuracy = 0
    k = 0
    for traincv, testcv in cv:
        classifier = nltk.NaiveBayesClassifier.train(train_set[traincv[0]:traincv[len(traincv)-1]])
        acc = nltk.classify.util.accuracy(classifier, train_set[testcv[0]:testcv[len(testcv)-1]])
        sum_accuracy += acc
        k += 1
        print str(k) + ')accuracy:', acc
    print 'AVERAGE ACCURACY: ' + str(sum_accuracy/k)


if __name__ == '__main__':
    tweets_read = []
    hashtags_read = []
    read_file()
    train_model(tweets_read, hashtags_read)


