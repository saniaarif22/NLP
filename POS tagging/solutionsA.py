from __future__ import division
import math
import nltk
import time
from collections import Counter
from math import log

# Constants to be used by you when you fill the functions
START_SYMBOL = '* '
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    #Unigram
    words = []
    for sentence in training_corpus:
	sent = sentence.split()
	for w in sent:
	    words.append(w);
	words.append(STOP_SYMBOL);
    #counting each word in words and storing in a dict
    unigram_p={}
    unigram_count = Counter(words)
    for word in unigram_count:
	unigram_p[word] = log(unigram_count[word]*1.0/len(words),2)    
    print unigram_p['near']
    #Bigram
    training_corpus = [end.replace('\n', STOP_SYMBOL) for end in training_corpus]
    training_corpus = [START_SYMBOL + line for line in training_corpus]
    bi_words = []
    for sentence in training_corpus:
        bi_sent = sentence.split()
	for w in bi_sent:
            bi_words.append(w);
     
    uni = Counter(bi_words)
    bigram_tuples = list(nltk.bigrams(bi_words))
    bigram_count = Counter(bigram_tuples)
    bigram_p = {}
    for big in bigram_count:
	bigram_p[big] = log(bigram_count[big]*1.0/uni[big[0]],2)
    print bigram_p['near', 'the']

    #Trigram
    training_corpus = [START_SYMBOL + line for line in training_corpus]
    tri_words = []
    for sentence in training_corpus:
        tri_sent = sentence.split()
        for w in tri_sent:
            tri_words.append(w);

    trigram_tuples = list(nltk.trigrams(tri_words))    
    trigram_p = Counter(trigram_tuples)
    for tri in trigram_p:
	if tri[0] == '*' and tri[1] =='*':
	    trigram_p[tri] = log(trigram_p[tri]*1.0/ len(training_corpus),2)
	else:
	    trigram_p[tri] = log(trigram_p[tri]*1.0/ bigram_count[tri[0], tri[1]],2)
    print trigram_p['near', 'the', 'ecliptic']
    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p, n, corpus):
    scores = []
    if n==1:
    	for sentence in corpus:
	    words = sentence.split();
	    prob=0
	    for w in words:
	    	prob = prob + ngram_p[w]
	    prob = prob + ngram_p[STOP_SYMBOL]
	    scores.append(prob)
    
    elif n==2:
	corpus = [START_SYMBOL + line for line in corpus]
	corpus = [end.replace('\n', STOP_SYMBOL) for end in corpus]
	words=[]
	for sentence in corpus:
	    words = sentence.split()
	    bigrams = list(nltk.bigrams(words))
	    prob =0
	    for b in bigrams:
		prob = prob + ngram_p[b]
	    scores.append(prob)

    else:
	corpus = [START_SYMBOL+ START_SYMBOL + line for line in corpus]
	corpus = [end.replace('\n', STOP_SYMBOL) for end in corpus]
	words =[]
	for sentence in corpus:
             words = sentence.split()
             trigrams = list(nltk.trigrams(words))
             prob =0
             for t in trigrams:
                prob = prob + ngram_p[t]
	     scores.append(prob)
	
    return scores

# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    corpus = [START_SYMBOL+ START_SYMBOL + line for line in corpus]
    corpus = [end.replace('\n', STOP_SYMBOL) for end in corpus]
    words=[]
    scores=[]
    lam = 1/3.0
    for sentence in corpus:
             words = sentence.split()
             tries = list(nltk.trigrams(words))
	     sum = 0
	     uni_s=0
	     bi_s=0
	     tri_s=0
	     f=0
	     for tri in tries:
		if tri[2] not in unigrams:
                     uni_s=float(MINUS_INFINITY_SENTENCE_LOG_PROB)
                     f=1
		if (tri[1],tri[2]) not in bigrams:
                     bi_s=float(MINUS_INFINITY_SENTENCE_LOG_PROB)
		     f=1
		if tri not in trigrams:
		     tri_s=float(MINUS_INFINITY_SENTENCE_LOG_PROB)
		     f=1
		if f==1:
		     if bi_s ==float(MINUS_INFINITY_SENTENCE_LOG_PROB):
			if uni_s==float(MINUS_INFINITY_SENTENCE_LOG_PROB):
			     sum =float(MINUS_INFINITY_SENTENCE_LOG_PROB)
			     break
			else:
			     totScore=math.log(math.pow(2,unigrams[(tri[2])])/3,2)
		     else:
			totScore=math.log((math.pow(2,unigrams[(tri[2])]))+(math.pow(2,bigrams[(tri[1],tri[2])]))/3,2)
		else:
		     totScore=math.log(((math.pow(2, unigrams[(tri[2])])) + (math.pow(2, bigrams[(tri[1],tri[2])])) + (math.pow(2,trigrams[tri])))/3, 2)
		sum = sum + totScore
	     scores.append(float(sum))
    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
