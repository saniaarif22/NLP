import theano
import theano.tensor as T

import numpy as np

class LogisticRegression:
    
    def __init__(self, dimension, num_classes):
        X = T.matrix('X')
        y = T.ivector('y')
        learning_rate = T.scalar('learning_rate')
        
        # initialize with 0 the weights W as a matrix
        self.W = theano.shared(value=np.zeros((dimension, num_classes),
                                                 dtype=theano.config.floatX),
                               name='W',
                               borrow=True)

        # initialize the biases b as a vector of 0s
        self.b = theano.shared(value=np.zeros((num_classes,),
                                                 dtype=theano.config.floatX),
                               name='b',
                                borrow=True)

        self.params = [self.W, self.b]
	
	#***Changed Here:***
	#self.input = dimension
	self.p_y_given_x = T.nnet.softmax(T.dot(X, self.W) + self.b)
	self.y_pred = T.argmax(self.p_y_given_x, axis=1)
	       
   	cost = -T.mean(T.log(self.p_y_given_x)[T.arange(y.shape[0]), y])
	g_W = T.grad(cost=cost, wrt=self.W)
    	g_b = T.grad(cost=cost, wrt=self.b)
	updates = [(self.W, self.W - learning_rate * g_W), (self.b, self.b - learning_rate * g_b)]
        
	#compile a theano function self.train that takes the matrix X, vector y, and learning rate as input
	self.train = theano.function(
        	inputs=[X, y, learning_rate],
        	outputs=cost,
        	updates=updates
    			)

        #compile a theano function self.predict that takes a matrix X as input and returns a vector y of predictions
	self.predict = theano.function(
        	inputs=[X],
        	outputs=self.y_pred) 

    def fit(self, X, y, num_epochs=5, learning_rate=0.05, verbose=False):
        for i in range(num_epochs):
            cost = self.train(X, y, learning_rate)
            if verbose:
                print('cost at epoch {}: {}'.format(i, cost))

    
