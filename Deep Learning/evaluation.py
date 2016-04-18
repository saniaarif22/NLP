from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import precision_recall_fscore_support, accuracy_score

from nltk.corpus import stopwords

def validate(classifier, dependencyData, dependencyRNN, corpus):
    train = dependencyData.transform(corpus.train)
    train_labels = zip(*train)[-1]
    train = zip(*zip(*train)[:-1])
    train_features = dependencyRNN.transform(train,
                                             dependencyData.stop_indices(stopwords.words('english')))
    print(train_features.shape)
    
    dev = dependencyData.transform(corpus.dev)
    dev_labels = zip(*dev)[-1]
    dev = zip(*zip(*dev)[:-1])
    dev_features = dependencyRNN.transform(dev,
                                           dependencyData.stop_indices(stopwords.words('english')))
    print(dev_features.shape)
    
    classifier.fit(train_features,
                   train_labels)

    train_predict = classifier.predict(train_features)
    dev_predict = classifier.predict(dev_features)

    train_accuracy = accuracy_score(train_labels, train_predict)
    dev_accuracy = accuracy_score(dev_labels, dev_predict)

    print('train acc = {}, val acc = {}'.format(train_accuracy, dev_accuracy))
    
    precision,recall,fscore,support = precision_recall_fscore_support(dev_labels,
                                                                      dev_predict,
                                                                      average='micro')
    print('Micro Averaged:')
    print(precision)
    print(recall)
    print(fscore)

    precision,recall,fscore,support = precision_recall_fscore_support(dev_labels,
                                                                      dev_predict,
                                                                      average='macro')
    print('Macro Averaged:')
    print(precision)
    print(recall)
    print(fscore)


