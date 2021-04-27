from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
clf = SVC(kernel='linear', C=1).fit(X_train, y_train)
print(clf.score(X_test, y_test))
clf = DummyClassifier(strategy='most_frequent', random_state=0)
clf.fit(X_train, y_train)
DummyClassifier(random_state=0, strategy='most_frequent')
clf.score(X_test, y_test)
