import time
import argparse

import numpy as np

import gensim

from sklearn.metrics import precision_recall_fscore_support
from sklearn.linear_model import LogisticRegression

from dependencyData import DependencyData
from dependencyRNN import DependencyRNN
from corpus import Corpus
from evaluation import validate

if __name__ == '__main__':

    # command line arguments
    parser = argparse.ArgumentParser(description='QANTA: a question answering neural network \
                                     with trans-sentential aggregation')
    parser.add_argument('--data', help='location of dataset', default='data/hist_split.json')
    parser.add_argument('--We', help='location of word embeddings')
    parser.add_argument('--seed', type=int, help='seed to use for random number generator for initialization')
    parser.add_argument('--load')
    parser.add_argument('--save')
    parser.add_argument('--num_batches', type=int, default=25)
    parser.add_argument('--num_epochs', type=int, default=30)    
    parser.add_argument('-d' ,'--dimension', type=int, default=100)
    parser.add_argument('--wrong_ans', type=int, default=100)
    parser.add_argument('--do_val', type=int, default=10)    
    parser.add_argument('-agr', '--adagrad_reset',
                        help='reset sum of squared gradients after this many epochs',
                        type=int, default=3)
    
    args = parser.parse_args()

    #we would normally do a search on a held out set for this parameter
    lr = LogisticRegression(C=10)
    
    corpus = Corpus(args.data)

    dd = DependencyData()
    train,dev,devtest,test = dd.scan_vocab(corpus)

    print('number of training sentences: {}'.format(len(train)))
    print('number of validation sentences: {}'.format(len(dev)))
    print('number of dependency relations: {}'.format(len(dd.relations)))
    print('number of elements in vocabulary: {}'.format(len(dd.vocab)))
    print('number of unique answers: {}'.format(len(dd.answers)))
    
    We = None
    if args.We:
        model = gensim.models.Word2Vec.load(args.We)
        We = dd.match_embeddings(model)
        
    if not args.load:
        d = DependencyRNN(100,
                          len(dd.vocab),
                          len(dd.relations),
                          list(dd.answers.values()),
                          We)
    else:
        d = DependencyRNN.load(args.load)

    num_batches = args.num_batches
    num_epochs = args.num_epochs

    batch_size = len(train)/num_batches
    print('batch_size {}'.format(batch_size))
    for i in range(num_epochs):
        epoch_cost = 0.0
        for j in range(num_batches+1):
            batch = train[j*batch_size:(j+1)*batch_size]
            start = time.time()
            cost = d.train(batch, args.wrong_ans)
            print ("epoch: {} batch: {} cost: {} time: {}".format(i,
                                                                  j,
                                                                  cost,
                                                                  time.time()-start))
            epoch_cost += cost

        print ('done with epoch {}, epoch cost = {}'.format(i, epoch_cost))

        # reset adagrad weights
        if i % args.adagrad_reset == 0 and i != 0:
            d.reset_weights()

        if i % args.do_val == 0:
            validate(lr, dd, d, corpus)

    validate(lr, dd, d, corpus)

    if args.save is not None:
        d.save(args.save, dd.answers)

