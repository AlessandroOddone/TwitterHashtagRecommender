# se diversi tweet sono identici --> eliminarli (SPAM)
#rimuovere hashtag, punteggiatura, simboli strani, etc.
#se il tweet  vuoto dopo aver rimosso lo schifo, eliminare riga
#lasciare solo nomi, verbi, avverbi e aggettivi
#tradurre slang: vedere come fare
from os.path import expanduser
import csv


def read_file():
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "tweets.csv"
    with open(home + path_to_file + file_name, 'rb') as f:
        for row in csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL):
            tweets_read.append(row[0])
            hashtags_read.append(row[1])


def write_file(tweets, hashtags):
    home = expanduser("~")
    path_to_file = "/Desktop/NLP Project/"
    file_name = "training.csv"
    rows = [[tweets[i], hashtags[i]] for i in range(0, len(tweets))]
    with open(home + path_to_file + file_name, 'ab') as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(rows)


def process(tweets):
    return tweets

if __name__ == '__main__':
    tweets_read = []
    hashtags_read = []
    read_file()
    tweets_processed = process(tweets_read)
    write_file(tweets_processed, hashtags_read)