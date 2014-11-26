from sklearn import metrics
import csv
import pickle
from collections import defaultdict
from os.path import expanduser
from operator import itemgetter


HASHTAGS_LIST = ['#dwts', '#glee', '#idol', '#xfactor', '#news', '#fashion', '#health', '#fail', '#jobs', '#business',
                 '#sales', '#economy', '#marketing', '#socialmedia', '#startup', '#edtech', '#education', '#teachers',
                 '#climate', '#solar', '#globalwarming', '#socialgood', '#cause', '#volunteer', '#4change']


def load_model():
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "model.pickle"
    with open(home + path_to_file + file_name, 'rb') as f:
        classifier = pickle.load(f)
        f.close()
    return classifier


def load_validation_set():
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "validation.csv"
    validation_set = []
    with open(home + path_to_file + file_name, 'rb') as f:
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL):
            validation_set.append(row)
    return validation_set


def unigrams(tweet):
    features = defaultdict(list)
    words = tweet.split()
    for w in words:
        features[w] = True
    return features


def feature_extractor(tweet):
    return unigrams(tweet)


def extract_features(tweet):
    features = defaultdict(list)
    words = tweet.split()
    for w in words:
        features[w] = True
    return features


def evaluate_model(classifier, validation_set):
    y_true = []
    y_pred = []

    #calculate the total accuracy of the model on validation data
    for i in range(len(validation_set)):
        y_true.append(validation_set[i][1])
        y_pred.append(classifier.classify(extract_features(validation_set[i][0])))
    print('TRUE LABELS: ' + str(y_true))
    print('PREDICTED LABELS: ' + str(y_pred))
    print('')

    total_accuracy = metrics.accuracy_score(y_true, y_pred)
    print("TOTAL ACCURACY: " + str(total_accuracy))
    print('')

    #calculate the total top3-accuracy of the model on validation data
    correctly_classified = 0
    for i in range(len(validation_set)):
        dist = classifier.prob_classify(extract_features(validation_set[i][0]))
        predicted_probs = []
        for label in dist.samples():
            predicted_probs.append((label, dist.prob(label)))
        predicted_probs = sorted(predicted_probs, key=itemgetter(1), reverse=True)
        #if the correct label is in the top3 of our classifier, count as correctly classified
        for j in range(3):
            if validation_set[i][1] in predicted_probs[j][0]:
                correctly_classified += 1
                break
    print("TOP3 TOTAL ACCURACY: " + str(float(correctly_classified)/float(len(validation_set))))
    print('')

    #calculate precision for each hashtag
    for hashtag in HASHTAGS_LIST:
        hashtag = hashtag.replace('#', '')
        validation_set_filtered = []
        for row in validation_set:
            if hashtag in row[1]:
                validation_set_filtered.append(row)
        y_true_h = []
        y_pred_h = []
        for i in range(len(validation_set_filtered)):
            y_true_h.append(validation_set_filtered[i][1])
            y_pred_h.append(classifier.classify(extract_features(validation_set_filtered[i][0])))
        precision_h = metrics.accuracy_score(y_true_h, y_pred_h)
        print('#' + hashtag + ': precision = ' + str(precision_h) +
              ' (support = ' + str(len(validation_set_filtered)) + ')')
        print('')

    #calculate top3 precision for each hashtag
    for hashtag in HASHTAGS_LIST:
        hashtag = hashtag.replace('#', '')
        validation_set_filtered = []
        for row in validation_set:
            if hashtag in row[1]:
                validation_set_filtered.append(row)
        for i in range(len(validation_set_filtered)):
            dist = classifier.prob_classify(extract_features(validation_set_filtered[i][0]))
            predicted_probs = []
            for label in dist.samples():
                predicted_probs.append((label, dist.prob(label)))
            predicted_probs = sorted(predicted_probs, key=itemgetter(1), reverse=True)
            #if the correct label is in the top3 of our classifier, count as correctly classified
            correctly_classified = 0
            for j in range(3):
                if validation_set_filtered[i][1] in predicted_probs[j][0]:
                    correctly_classified += 1
                    break
        print('#' + hashtag + ': top3 precision = ' + str(float(correctly_classified)/float(len(validation_set_filtered))) +
              ' (support = ' + str(len(validation_set_filtered)) + ')')
        print('')


if __name__ == '__main__':
    model = load_model()
    evaluate_model(model, load_validation_set())