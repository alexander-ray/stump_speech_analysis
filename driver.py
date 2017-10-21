import json
import os

import pickle
import numpy as np
from urllib.request import urlopen
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, precision_score
import matplotlib.pyplot as plt

from speech_scraper import remarks_driver

def main():
    #clinton_remarks_test = []
    #clinton_remarks_train = []
    obama1_remarks_test = []
    obama1_remarks_train = []
    obama2_remarks_test = []
    obama2_remarks_train = []
    #filenames = {'clinton_remarks_test': clinton_remarks_test,
    #            'clinton_remarks_train': clinton_remarks_train,
    #            'obama_remarks_test': obama_remarks_test,
    #            'obama_remarks_train': obama_remarks_train}
    filenames = {'obama1_remarks_test': obama1_remarks_test,
                'obama1_remarks_train': obama1_remarks_train,
                'obama2_remarks_test': obama2_remarks_test,
                'obama2_remarks_train': obama2_remarks_train}

    exists = True
    for key, _ in filenames.items():
        if (not os.path.isfile('./' + key)):
            exists = False

    if (not exists):
        remarks_driver()

    for key, _ in filenames.items():
        with open(key) as json_file:
            filenames[key] = json.load(json_file)

    train = filenames['obama1_remarks_train'] + filenames['obama2_remarks_train']
    D = np.array(train)
    Y = D[:, 0]
    v = CountVectorizer(stop_words='english', analyzer='word')
    X = v.fit_transform(D[:,1])
    feature_names = np.asarray(v.get_feature_names())

    test = filenames['obama1_remarks_test'] + filenames['obama2_remarks_test']
    D_test = np.array(test)
    Y_test = D_test[:,0]
    X_test = v.transform(D_test[:,1])

    print("Number of training instances: %d" % (D.shape[0]))
    print("Number of test instances: %d" % (D_test.shape[0]))

    alpha_arr = [0.0001,0.001,0.01,0.1,1.0,10.0,100.0]

    train_acc = []
    test_acc = []
    for a in alpha_arr:
        classifier = SGDClassifier(loss='log', max_iter=1000, tol=1.0e-12, random_state=123, alpha=a)
        classifier.fit(X, Y)
        # Add to accuracy lists
        train_acc.append(accuracy_score(Y, classifier.predict(X)))
        test_acc.append(accuracy_score(Y_test, classifier.predict(X_test)))

    plt.figure(1)
    plt.plot(alpha_arr, train_acc, color='blue', lw=2, marker='o', label="Training Accuracy")
    plt.plot(alpha_arr, test_acc, color='red', lw=2, marker='o', label="Testing Accuracy")

    ax = plt.gca()
    ax.set_xscale('log')

    plt.xlabel("Alpha")
    plt.ylabel("Accuracy")
    plt.title("3.1: Alpha vs Accuracy Linear Regression")
    plt.legend(loc='upper right')
    plt.show()

    print("\nFeature weights:")
    args = np.argsort(classifier.coef_[0])
    for a in args[0:20]:
        print(" %s: %0.4f" % (feature_names[a], classifier.coef_[0][a]))

if __name__ == '__main__':
    main()
