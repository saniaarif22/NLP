import argparse

import numpy as np
from sklearn import datasets
from sklearn.metrics import classification_report

import logisticRegression

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--lr', action='store_true')

    args = parser.parse_args()

    if args.lr:
        digits = datasets.load_digits()

        lr = logisticRegression.LogisticRegression(digits.data.shape[1],
                                                   np.unique(digits.target).shape[0])

        num_data = digits.data.shape[0]
        lr.fit(digits.data[:num_data//2],
               digits.target[:num_data//2].astype(np.int32),
               num_epochs=100,
               verbose=True)
        y_pred = lr.predict(digits.data[num_data//2:].astype(np.int32))

        print('classification report: {}'.format(classification_report(digits.target[num_data//2:],
                                                                       y_pred)))

        
