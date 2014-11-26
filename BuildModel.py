import nltk
from sklearn import cross_validation
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle
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
    sum_average_precision = 0
    sum_f1 = 0
    sum_precision = 0
    sum_recall = 0
    sum_roc_auc = 0
    k = 0
    for traincv, testcv in cv:
        #classifier = nltk.NaiveBayesClassifier.train(train_set[traincv[0]:traincv[len(traincv)-1]])
        classifier = nltk.MaxentClassifier.train(train_set[traincv[0]:traincv[len(traincv)-1]], max_iter=50)
        #classifier = nltk.SklearnClassifier(LogisticRegression()).train(train_set[traincv[0]:traincv[len(traincv)-1]])
        #classifier = nltk.SklearnClassifier(SVC(kernel='linear', probability=True)).train(train_set[traincv[0]:traincv[len(traincv)-1]])

        y_true = []
        y_pred = []
        for i in range(len(testcv)):
            y_true.append(train_set[testcv[i]][1])
            y_pred.append(classifier.classify(train_set[testcv[i]][0]))

        acc = metrics.accuracy_score(y_true, y_pred)
        sum_accuracy += acc

        k += 1
        print(str(k) + ')accuracy: ' + str(acc))
        print('true labels: ' + str(y_true))
        print('predicted labels: ' + str(y_pred))
        print('')
    print ('ACCURACY: ' + str(sum_accuracy/k))
    classifier.train(train_set, max_iter=100)
    return classifier


def save_model(classifier):
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "model.pickle"
    with open(home + path_to_file + file_name, 'wb') as f:
        pickle.dump(classifier, f)
        f.close()


if __name__ == '__main__':
    tweets_read = []
    hashtags_read = []
    read_file()
    save_model(train_model(tweets_read, hashtags_read))


