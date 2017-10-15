import json
import os

import pickle
import numpy as np
from urllib.request import urlopen
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, precision_score
import matplotlib.pyplot as plt

from speech_scraper import remarks_driver

def main():
    clinton_remarks_test = []
    clinton_remarks_train = []
    obama_remarks_test = []
    obama_remarks_train = []
    filenames = {'clinton_remarks_test': clinton_remarks_test,
                'clinton_remarks_train': clinton_remarks_train,
                'obama_remarks_test': obama_remarks_test,
                'obama_remarks_train': obama_remarks_train}

    exists = True
    for key, _ in filenames.items():
        if (not os.path.isfile('./' + key)):
            exists = False

    if (not exists):
        remarks_driver()

    for key, _ in filenames.items():
        with open(key) as json_file:
            filenames[key] = json.load(json_file)

    train = filenames['clinton_remarks_train'] + filenames['obama_remarks_train']
    D = np.array(train)
    Y = D[:, 0]
    v = DictVectorizer(sparse=True)
    X = v.fit_transform(D[:,1])
    feature_names = np.asarray(v.get_feature_names())

    test = filenames['clinton_remarks_test'] + filenames['obama_remarks_test']
    D_test = np.array(test)
    Y_test = D_test[:,0]
    X_test = v.transform(D_test[:,1])

    print("Number of training instances: %d" % (D.shape[0]))
    print("Number of test instances: %d" % (D_test.shape[0]))

    alpha = 0.001
    classifier = SGDClassifier(loss='log', max_iter=1000, tol=1.0e-12, random_state=123, alpha=alpha)
    classifier.fit(X, Y)

    print("\nFeature weights:")
    args = np.argsort(classifier.coef_[0])
    for a in args:
        print(" %s: %0.4f" % (feature_names[a], classifier.coef_[0][a]))
if __name__ == '__main__':
    main()
