from nltk.corpus import comtrans
import A
import B
import EC
import time

if __name__ == '__main__':
    time.clock()
    aligned_sents = comtrans.aligned_sents()[:350]
    A.main(aligned_sents)
    print "Part A time: " + str(time.clock()) + ' sec'
    #A.testmain(aligned_sents)
    B.main(aligned_sents)
    print "Part B time: " + str(time.clock()) + ' sec'
    EC.main(aligned_sents)
