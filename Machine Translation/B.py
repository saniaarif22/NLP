from __future__ import division
from collections import defaultdict
from nltk.align.ibm1 import IBMModel1
from nltk.align import AlignedSent
from nltk.align import Alignment
import A

class BerkeleyAligner():

    def __init__(self, align_sents, num_iter):
        self.t, self.q = self.train(align_sents, num_iter)

    # Computes the alignments for align_sent, using this model's parameters. Return
    #       an AlignedSent object, with the sentence pair and the alignments computed.
    def align(self, align_sent):
	if self.t is None or self.q is None:
            raise ValueError("No parameters trained")
	#MIN_PROB = 1.0e-12	
	wordlen = align_sent.words.__len__()
	motslen = align_sent.mots.__len__()
	alignment = []
	
	for i, en_word in enumerate(align_sent.words):
		max_align = (self.t[en_word][None] * self.q[0][i+1][wordlen][motslen], None)
		for j, ge_word in enumerate(align_sent.mots):
			align_prob = (self.t[en_word][ge_word] * self.q[j+1][i+1][wordlen][motslen], j)
			if align_prob >= max_align:
				max_align = align_prob
				best_pt = j
		alignment.append((i, best_pt))   

	return AlignedSent(align_sent.words, align_sent.mots, Alignment(alignment)) #uses built-in Alignment func

    # Implement the EM algorithm. num_iters is the number of iterations. Returns the 
    # translation and distortion parameters as a tuple.
    def train(self, aligned_sents, num_iters):
	aligned_invert = []
	MIN_PROB = 1.0e-12
	#find initial probabilities
	t_reg = IBMModel1(aligned_sents, 4).probabilities
	
	for sent in aligned_sents:
		aligned_invert.append(sent.invert())

	t_inv = IBMModel1(aligned_invert, 8).probabilities	
	
	t = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB))))
	dalign = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB))))
	
	#Eng and Ger vocabs
	eng = set()
	ger = set()
	for aligned_sent in aligned_sents:
		eng.update(aligned_sent.words)
		ger.update(aligned_sent.mots)
	eng.add(None)
	ger.add(None)
	
	#Initialization	
	for aligned_sent in aligned_sents:
		en = [None] + aligned_sent.words
		ge = [None] + aligned_sent.mots
		l_en = len(en) -1
		l_ge = len(ge) -1
		x = 1/ (l_ge + 1)
		for i in range(0, l_ge+1):
			for j in range(1, l_en+1):
				t[i][j][l_en][l_ge] = x

		y = 1/ (l_en + 1)
		for i in range(0, l_en+1):
			for j in range(1, l_ge+1):
				dalign[i][j][l_ge][l_en] = y

	#EM:
	for k in xrange(num_iters):
		ef_count = defaultdict(lambda: defaultdict(lambda: MIN_PROB))
            	fe_count = defaultdict(lambda: defaultdict(lambda: MIN_PROB))
            	f_total = defaultdict(lambda: MIN_PROB)
            	count_align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB))))
            	total_align = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB)))
            	count_align_r = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB))))
            	total_align_r = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB)))
            	e_total = defaultdict(lambda: MIN_PROB)
            	deno = defaultdict(lambda: MIN_PROB)
            	deno_r = defaultdict(lambda: MIN_PROB)	
		
		for aligned_sent in aligned_sents:
			en = [None] + aligned_sent.words
                	ge = [None] + aligned_sent.mots
                	l_en = len(en) -1
                	l_ge = len(ge) -1
			
			#denominators
			for i in xrange(1, l_en + 1):
				en_word = en[i]
				deno[en_word] = 0
				for j in xrange(0, l_ge + 1):
					deno[en_word] += t_reg[en_word][ge[j]] * t[j][i][l_en][l_ge]

			for i in xrange(1, l_ge + 1):
				ge_word = ge[i]
				deno_r[ge_word] = 0
				for j in xrange(0, l_en + 1):
					deno_r[ge_word] += t_inv[ge_word][en[j]] * dalign[j][i][l_ge][l_en]		

			#counting
			for i in xrange(1, l_en + 1):
				en_word = en[i]
				for j in xrange(l_ge + 1):
					ge_word = ge[j]
					delta = t[j][i][l_en][l_ge] * t_reg[en_word][ge_word] / deno[en_word]
					ef_count[en_word][ge_word] += delta
					f_total[ge_word] += delta
					count_align[j][i][l_en][l_ge] += delta
					total_align[i][l_en][l_ge] += delta

			for i in xrange(1, l_ge + 1):
                                ge_word = ge[i]
                                for j in xrange(l_en + 1):
                                        en_word = en[j]
                                        delta = dalign[j][i][l_ge][l_en] * t_inv[ge_word][en_word] / deno_r[ge_word]
                                        fe_count[ge_word][en_word] += delta
                                        e_total[en_word] += delta
                                        count_align_r[j][i][l_ge][l_en] += delta
                                        total_align_r[i][l_ge][l_en] += delta
		#Avg count
		for en in ef_count:
			for ge in ef_count[en]:
				ef_count[en][ge] = (ef_count[en][ge] + fe_count[ge][en]) /2
				fe_count[ge][en] = ef_count[en][ge]

		for aligned_sent in aligned_sents:
			src = [None] + aligned_sent.words
			tar = [None] + aligned_sent.mots
			l_src = len(src) -1
			l_tar = len(tar) -1
			for i in xrange(1, l_src +1):
				for j in xrange(l_tar +1):
					count_align[j][i][l_src][l_tar] = (count_align[j][i][l_src][l_tar] + count_align_r[i][j][l_tar][l_src]) / 2
	                       		count_align_r[i][j][l_tar][l_src] = count_align[j][i][l_src][l_tar]

		#Probability estimation
		t_reg = defaultdict(lambda: defaultdict(lambda: MIN_PROB))
            	t = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB))))
            	t_inv = defaultdict(lambda: defaultdict(lambda: MIN_PROB))
            	dalign = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: MIN_PROB))))
		
		#lex trans probabilities
		for i in ger:
			for  j in eng:
				t_reg[j][i] = ef_count[j][i] / f_total[i]

		for i in eng:
			for j in ger:
				t_inv[j][i] = fe_count[j][i] / e_total[i]

		#alignment probabilities
		for aligned_sent in aligned_sents:
			en = [None] + aligned_sent.words
			ge = [None] + aligned_sent.mots
			l_en = len(en) - 1
			l_ge = len(ge) - 1
			
			for i in xrange(0, l_ge + 1):
				for j in xrange(1, l_en + 1):
					t[i][j][l_en][l_ge] = count_align[i][j][l_en][l_ge] / total_align[j][l_en][l_ge]

			for i in xrange(0, l_en + 1):
                                for j in xrange(1, l_ge + 1):
                                        dalign[i][j][l_ge][l_en] = count_align_r[i][j][l_ge][l_en] / total_align_r[j][l_ge][l_en]  

        return (t_reg, t)

def main(aligned_sents):
    ba = BerkeleyAligner(aligned_sents, 10)
    A.save_model_output(aligned_sents, ba, "ba.txt")
    avg_aer = A.compute_avg_aer(aligned_sents, ba, 50)

    print ('Berkeley Aligner')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
