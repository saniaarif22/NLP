import json

import numpy as np
import gensim

from adagrad import Adagrad

json_data=open('hist_split.json').read()
parsed_data = json.loads(json_data)

train_data = parsed_data["train"]
sentences = []

for list in train_data:
	needed = list[0]
	words = []
	for subl in needed:
		if subl[0] == None:
			words.append("*")
		else:	
			words.append(subl[0])
	sentences.append(words)	

model = gensim.models.Word2Vec(size=100, window=5, min_count=1)
model.build_vocab(sentences)
alpha, min_alpha, passes = (0.025, 0.001, 20)
alpha_delta = (alpha - min_alpha) / passes
#model.save('mymodel')

for epoch in range(passes):
	model.alpha, model.min_alpha = alpha, alpha
	model.train(sentences)

	print('completed pass %i at alpha %f' % (epoch + 1, alpha))
	alpha -= alpha_delta

	np.random.shuffle(sentences)

model.save('buildmodel')
