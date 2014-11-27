import csv
from os.path import expanduser
from sklearn.cross_validation import train_test_split


def load_file():
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "tweets.csv"
    data = []
    with open(home + path_to_file + file_name, 'rb') as f:
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL):
            data.append(row)
    return data


def divide_dataset(data):
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    validation_file_name = "validation_original.csv"
    train_file_name = "training_original.csv"

    train_new, validation_new = train_test_split(data, test_size=0.1, random_state=42)

    with open(home + path_to_file + train_file_name, 'wb') as train_file,\
            open(home + path_to_file + validation_file_name, 'wb') as validation_file:
        csv.writer(train_file, quoting=csv.QUOTE_ALL).writerows(train_new)
        csv.writer(validation_file, quoting=csv.QUOTE_ALL).writerows(validation_new)


if __name__ == '__main__':
    dataset = load_file()
    divide_dataset(dataset)