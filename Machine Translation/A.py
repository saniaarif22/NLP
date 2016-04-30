import nltk
from nltk.align.ibm1 import IBMModel1
from nltk.align.ibm2 import IBMModel2

# Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
	return IBMModel1(aligned_sents, 10)


# Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
	return IBMModel2(aligned_sents, 10)


# Compute the average AER for the first n sentences
# in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
	aer = []
    	for i in xrange(n):
        	aligned_words = model.align(aligned_sents[i])
        	aer.append(aligned_sents[i].alignment_error_rate(aligned_words))
    	return (0.0 + sum(aer)) / aer.__len__()

# Computes the alignments for the first 20 sentences in
# aligned_sents and saves the sentences and their alignments
# to file_name in the format:
# words
# mots
# alignment
# (blank line)
def save_model_output(aligned_sents, model, file_name):
	
	#open file to write into
	f = open(file_name,'w')
   	for i in xrange(20):
        	res = model.align(aligned_sents[i])
        	words = str(res.words)  
        	mots = str(res.mots)
        	align = str(res.alignment)
        	f.write(words+'\n'+mots+'\n'+align+'\n'+'\n')
    
    	f.close()


def main(aligned_sents):
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))

    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))


#For different iterations
def testmain(aligned_sents):
	for n in range(19, 20):
		print ('%s\n'%(n))
		ibm1 = IBMModel1(aligned_sents, n)
    		avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    		print ('IBM Model 1')
    		print ('---------------------------')
    		print('Average AER: {0:.3f}\n'.format(avg_aer))

    		ibm2 = IBMModel2(aligned_sents, n)
    		avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)

    		print ('IBM Model 2')
    		print ('---------------------------')
    		print('Average AER: {0:.3f}\n'.format(avg_aer))
