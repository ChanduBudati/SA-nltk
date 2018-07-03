'''
Name: Chandu Budati
CSCI 6350-001
Project#3
Due: 26, Feb, 2018
'''

from math import floor
import nltk
from nltk.corpus import opinion_lexicon
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

ps = PorterStemmer()
negwords = opinion_lexicon.words("negative-words.txt")[:]
poswords = opinion_lexicon.words("positive-words.txt")[:]

#Thought of stemming first, but corpus contained all possible variations of the words so, removed it later.
#negwords = [ps.stem(i) for i in opinion_lexicon.words("negative-words.txt")]
#print(r)
stop_words = set(stopwords.words('english'))

negations = ["neither", "nor" , "not", "dont", "is'nt", "does'nt", "aint", "ai'nt"]

notintense = ["little", "few", "hardly", "rarely", "scarcely", "seldom"]

intense = ["extremely", "exceedingly", "exceptionally", "extraordinarily", "tremendously",
           "immensely", "hugely", "intensely", "acutely", "abundantly", "uncommonly", "decidedly",
           "particularly", "highly", "remarkably", "really", "very"]

#takes in one reiview str and returns rating
def rate(rev):
    pos = 0
    neg = 0
    mul = 1
    n = 0
    rev = word_tokenize(rev)
    rev = [i.lower() for i in rev if i.lower not in stop_words]
    for word in rev:
        #checking for intensity and negation words
        if word in notintense:
            mul = 0.5
        elif word in intense:
            mul = 1.5
        elif word in negations:
            n = (n+1)%2
        elif word in [".", ",", "..."]:
            n = 0
        #updating score based on presence of words
        elif word in poswords:
            if n == 1:
                neg += mul
            else:
                pos += mul
            mul = 1

        elif word in negwords:
            if n == 1:
                pos += mul
            else:
                neg += mul
            mul = 1
    #normalizing score
    if pos+neg == 0:
        score = 3
    else:
        score = floor(2*(pos/(pos+neg))) - floor(2*(neg/(pos+neg))) + 3
    return score

def main():

    with open('reviews.txt', 'r') as content_file:
        content = content_file.read()

    content = content.split("\n\n")
    i = 1
    for rev in content:
        res = rate(rev)
        print("review #"+str(i)+" - "+str(res))
        i += 1
main()