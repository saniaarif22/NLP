import numpy as np
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
from dependencyRNN import DependencyRNN

#loading answer embeddings
random = DependencyRNN.load("random_init.npz")
#answer embedding produces dictionary
keys = random.answers.keys() #words
X = random.answers.values()
x = []
y = []

#Given:
model = TSNE(n_components=2, perplexity=30.0)
reduced = model.fit_transform(X)

for i in range(0, len(keys)):
	x.append(reduced[i][0])
	y.append(reduced[i][1])

plt.scatter(x,y)
bbox_props = dict(boxstyle="rarrow,pad=0.3", fc="cyan")
for i in range(0, len(keys)):
	plt.annotate(keys[i], xy=(x[i],y[i]),bbox=bbox_props)

plt.show()
#np.set_printoptions(suppress=True)
#model.fit_transform(X)
