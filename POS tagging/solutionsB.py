import sys
import nltk
import math
import time
from collections import Counter

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000


# TODO: IMPLEMENT THIS FUNCTION
# Receives a list of tagged sentences and processes each sentence to generate a list of words and a list of tags.
# Each sentence is a string of space separated "WORD/TAG" tokens, with a newline character in the end.
# Remember to include start and stop symbols in yout returned lists, as defined by the constants START_SYMBOL and STOP_SYMBOL.
# brown_words (the list of words) should be a list where every element is a list of the tags of a particular sentence.
# brown_tags (the list of tags) should be a list where every element is a list of the tags of a particular sentence.
def split_wordtags(brown_train):
    brown_words = []
    brown_tags = []
    for sentence in brown_train:
	bw = []
	bt = []
	bw.append(START_SYMBOL)
	bw.append(START_SYMBOL)
	bt.append(START_SYMBOL)
	bt.append(START_SYMBOL)
	wordtags = sentence.split()
	for wordtag in wordtags:
	    word = wordtag.rsplit('/',1)
	    bw.append(word[0])
	    bt.append(word[1])
	bw.append(STOP_SYMBOL)
        bt.append(STOP_SYMBOL)
	brown_words.append(bw)
	brown_tags.append(bt)	
    return brown_words, brown_tags


# TODO: IMPLEMENT THIS FUNCTION
# This function takes tags from the training data and calculates tag trigram probabilities.
# It returns a python dictionary where the keys are tuples that represent the tag trigram, and the values are the log probability of that trigram
def calc_trigrams(brown_tags):
    q_values = {}
    brown = [val for sublist in brown_tags for val in sublist]
    
    uni = Counter(brown)
    #print uni

    bigram_tuples = list(nltk.bigrams(brown))
    bigram_count = Counter(bigram_tuples)
    #print bigram_count    

    trigram_tuples = list(nltk.trigrams(brown))
    trigram_p = Counter(trigram_tuples)
    #print trigram_p

    for tri in trigram_p:
        q_values[tri] = math.log(trigram_p[tri]*1.0/ bigram_count[tri[0], tri[1]],2)
    print q_values['CONJ', 'ADV', 'NOUN']
    print q_values['DET','NUM','NOUN']
    print q_values['NOUN','PRT','CONJ']

    return q_values

# This function takes output from calc_trigrams() and outputs it in the proper format
def q2_output(q_values, filename):
    outfile = open(filename, "w")
    trigrams = q_values.keys()
    trigrams.sort()  
    for trigram in trigrams:
        output = " ".join(['TRIGRAM', trigram[0], trigram[1], trigram[2], str(q_values[trigram])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and returns a set of all of the words that occur more than 5 times (use RARE_WORD_MAX_FREQ)
# brown_words is a python list where every element is a python list of the words of a particular sentence.
# Note: words that appear exactly 5 times should be considered rare!
def calc_known(brown_words):
    known_words = set([])
    brown = [val for sublist in brown_words for val in sublist]
    #print len(brown)
    count = Counter(brown)
    for word in count:
	if count.get(word) > RARE_WORD_MAX_FREQ:
	   known_words.add(word)
    #print len(known_words)
    return known_words

# TODO: IMPLEMENT THIS FUNCTION
# Takes the words from the training data and a set of words that should not be replaced for '_RARE_'
# Returns the equivalent to brown_words but replacing the unknown words by '_RARE_' (use RARE_SYMBOL constant)
def replace_rare(brown_words, known_words):
    brown_words_rare = []
    #brown = [val for sublist in brown_words for val in sublist]
    for sublist in brown_words:
	b = []
	for word in sublist:
	   if word not in known_words:
		b.append(RARE_SYMBOL)
	   else:
		b.append(word)
	brown_words_rare.append(b)
    #print brown_words_rare
    return brown_words_rare

# This function takes the ouput from replace_rare and outputs it to a file
def q3_output(rare, filename):
    outfile = open(filename, 'w')
    for sentence in rare:
        outfile.write(' '.join(sentence[2:-1]) + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates emission probabilities and creates a set of all possible tags
# The first return value is a python dictionary where each key is a tuple in which the first element is a word
# and the second is a tag, and the value is the log probability of the emission of the word given the tag
# The second return value is a set of all possible tags for this data set
def calc_emission(brown_words_rare, brown_tags):
    e_values = {}
    taglist = set([])
    tag_count = Counter([tag for sublist in brown_tags for tag in sublist])
    taglist = tag_count.keys()
    paircount={}
    for i in xrange(len(brown_words_rare)):
	sentence = brown_words_rare[i]
	for j in xrange(len(sentence)):
	    pair = (sentence[j], brown_tags[i][j])
	    paircount[pair] = paircount.get(pair, 0) + float(1)
    for tup,count in paircount.iteritems():
	    prob=float(count)/float(tag_count[tup[1]])
	    if prob==0:
		e_values[tup]=float(LOG_PROB_OF_ZERO)
	    else:
		e_values[tup]=math.log(prob,2)
    #print e_values['America','NOUN']
    #print e_values['Columbia','NOUN']
    #print e_values['New','ADJ']
    #print e_values['York','NOUN']
    print e_values['*','*']
    print e_values['midnight','NOUN']
    print e_values['Place', 'VERB']
    return e_values, taglist

# This function takes the output from calc_emissions() and outputs it
def q4_output(e_values, filename):
    outfile = open(filename, "w")
    emissions = e_values.keys()
    emissions.sort()  
    for item in emissions:
        output = " ".join([item[0], item[1], str(e_values[item])])
        outfile.write(output + '\n')
    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# This function takes data to tag (brown_dev_words), a set of all possible tags (taglist), a set of all known words (known_words),
# trigram probabilities (q_values) and emission probabilities (e_values) and outputs a list where every element is a tagged sentence 
# (in the WORD/TAG format, separated by spaces and with a newline in the end, just like our input tagged data)
# brown_dev_words is a python list where every element is a python list of the words of a particular sentence.
# taglist is a set of all possible tags
# known_words is a set of all known words
# q_values is from the return of calc_trigrams()
# e_values is from the return of calc_emissions()
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. Remember also that the output should not contain the "_RARE_" symbol, but rather the
# original words of the sentence!
def viterbi(brown_dev_words, taglist, known_words, q_values, e_values):
    tagged = []
    unique_tags = set(taglist)
    
    unique_tags.remove(START_SYMBOL)
    unique_tags.remove(STOP_SYMBOL)
    taglist = list(unique_tags)

    unique_known = set(known_words)
    count =0
    for sentence in brown_dev_words:
	word_tag = []
	sentence.insert(0, "WORD_NOT_REQUIRED")
	pi = {}
	backpointers = {}
	count = count + 1
	for i in xrange(1, len(sentence)):
	    curr = sentence[i]
	    #Rare words
	    if curr not in unique_known:
		curr= RARE_SYMBOL
	    #Getting 2 prev tags
	    prev2tag = find_tag(taglist, i-2)
	    prevtag = find_tag(taglist, i-1)
	    currtag = find_tag(taglist, i)
		
	    for x in prevtag:
		for y in currtag:
		    maxprob = -2000.0
		    for z in prev2tag:
			currprob = pi_value(pi, i-1, z, x) + q_values.get((z, x, y), LOG_PROB_OF_ZERO) + e_values.get((curr, y), LOG_PROB_OF_ZERO)
			if currprob >= maxprob or ((i, x, y) not in backpointers):
			    maxprob = currprob
			    backpointers[(i, x, y)] = z
			    pi[(i, x, y)] = currprob
	n = len(sentence) -1
	l = [None] * (len(sentence)) #tag sequence of the sentence
	last = find_tag(taglist, n)
	second_last = find_tag(taglist, n-1)
	maxlastprob = -2000.00
	for x in second_last:
	    for y in last:
		currprob = pi_value(pi, n, x, y) + q_values.get((x, y, STOP_SYMBOL), LOG_PROB_OF_ZERO)
		if currprob >= maxlastprob:
		    maxlastprob = currprob
		    l[len(l)-1] = y
		    l[len(l)-2] = x
	#Backtracking
	for k in reversed(xrange(1, n-1)):
		l[k] = backpointers[(k+2, l[k+1], l[k+2])]
	for i in xrange(1, len(sentence)):
		word_tag.append(sentence[i] + "/" + l[i])
	tagged.append(" ".join(word_tag) + "\n")
			
    return tagged

def find_tag(taglist, i):
    if i<1:
	return [START_SYMBOL]
    else:
	return taglist

def pi_value(pi, i, x, y):
    if x==START_SYMBOL and y==START_SYMBOL and i==0:
	return 0.0
    else:
	return pi.get((i, x, y), LOG_PROB_OF_ZERO)

# This function takes the output of viterbi() and outputs it to file
def q5_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
        outfile.write(sentence)
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# This function uses nltk to create the taggers described in question 6
# brown_words and brown_tags is the data to be used in training
# brown_dev_words is the data that should be tagged
# The return value is a list of tagged sentences in the format "WORD/TAG", separated by spaces. Each sentence is a string with a 
# terminal newline, not a list of tokens. 
def nltk_tagger(brown_words, brown_tags, brown_dev_words):
    # Hint: use the following line to format data to what NLTK expects for training
    training = [ zip(brown_words[i][2:-1],brown_tags[i][2:-1]) for i in xrange(len(brown_words)) ]    
    # print training
    # IMPLEMENT THE REST OF THE FUNCTION HERE
    tagged = []
    default_tagger= nltk.DefaultTagger('NOUN')
    #unigram_tagger = nltk.UnigramTagger(training, backoff=default_tagger)
    bigram_tagger = nltk.BigramTagger(training, backoff=default_tagger)
    trigram_tagger = nltk.TrigramTagger(training, backoff=bigram_tagger)
    for sentence in brown_dev_words:
	tag = trigram_tagger.tag(sentence)
	temp = []
	for t in tag:
		temp.append(t[0] + "/" + t[1])
	tagged.append(temp)
    return tagged

# This function takes the output of nltk_tagger() and outputs it to file
def q6_output(tagged, filename):
    outfile = open(filename, 'w')
    for sentence in tagged:
	s = ' '.join(sentence)+'\n'
        outfile.write(s)
    outfile.close()

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

def main():
    # start timer
    time.clock()

    # open Brown training data
    infile = open(DATA_PATH + "Brown_tagged_train.txt", "r")
    brown_train = infile.readlines()
    infile.close()

    # split words and tags, and add start and stop symbols (question 1)
    brown_words, brown_tags = split_wordtags(brown_train)

    # calculate tag trigram probabilities (question 2)
    q_values = calc_trigrams(brown_tags)

    # question 2 output
    q2_output(q_values, OUTPUT_PATH + 'B2.txt')

    # calculate list of words with count > 5 (question 3)
    known_words = calc_known(brown_words)

    # get a version of brown_words with rare words replace with '_RARE_' (question 3)
    brown_words_rare = replace_rare(brown_words, known_words)

    # question 3 output
    q3_output(brown_words_rare, OUTPUT_PATH + "B3.txt")

    # calculate emission probabilities (question 4)
    e_values, taglist = calc_emission(brown_words_rare, brown_tags)

    # question 4 output
    q4_output(e_values, OUTPUT_PATH + "B4.txt")

    # delete unneceessary data
    del brown_train
    del brown_words_rare

    # open Brown development data (question 5)
    infile = open(DATA_PATH + "Brown_dev.txt", "r")
    brown_dev = infile.readlines()
    infile.close()

    # format Brown development data here
    brown_dev_words = []
    brown_dev_words_2 = []
    for sentence in brown_dev:
        brown_dev_words.append(sentence.split(" ")[:-1])
	brown_dev_words_2.append(sentence.split(" ")[:-1])

    # do viterbi on brown_dev_words (question 5)
    viterbi_tagged = viterbi(brown_dev_words, taglist, known_words, q_values, e_values)

    # question 5 output
    q5_output(viterbi_tagged, OUTPUT_PATH + 'B5.txt')

    # do nltk tagging here
    nltk_tagged = nltk_tagger(brown_words, brown_tags, brown_dev_words_2)

    # question 6 output
    q6_output(nltk_tagged, OUTPUT_PATH + 'B6.txt')

    # print total time to run Part B
    print "Part B time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
