import nltk
import sys

greeting = sys.stdin.read()
print greeting

token_list = nltk.word_tokenize(greeting)
print "The tokens in the greeting are"
squirrel = 0
girl = 0

for token in token_list:
    print token
    if token.lower() == "squirrel":
	squirrel = squirrel + 1
    if token.lower() == "girl":
	girl = girl + 1
print "There were %d instances of the word 'squirrel' and %d instances of the word 'girl.'" % (squirrel, girl)
