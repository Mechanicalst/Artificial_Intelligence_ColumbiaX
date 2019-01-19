#importing the libraries
import argparse as argP
import numpy as np

#importing sklearn modules
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def main(input_file, output_file):
    raw_Dt = np.loadtxt(input_file, delimiter=',')
    fil_out = open(output_file, 'w')
    x = raw_Dt[:, :-1]
    y = raw_Dt[:, -1]
    
    # printraw_data[0]
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.4, random_state = 42)
    
    
    #defining parameters for linear
    params = {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100],
        'degree': [4, 5, 6],
        'gamma': [0.1, 1],
        'kernel': ['linear']
    }

    grid_thing = GridSearchCV(SVC(), params, n_jobs = 1)
    grid_thing.fit(x_train, y_train)
    fil_out.write("%s, %0.2f, %0.2f\n"%('svm_linear', grid_thing.best_score_, grid_thing.score(x_test, y_test)))
    
      #defining parameters for kernel svm
    params = {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100],
        'gamma': [0.1, 0.5, 1, 3, 6, 10],
        'kernel': ['rbf']
    }
    grid_thing = GridSearchCV(SVC(), params, n_jobs = 1)
    grid_thing.fit(x_train, y_train)
    fil_out.write("%s, %0.2f, %0.2f\n"%('svm_rbf', grid_thing.best_score_, grid_thing.score(x_test, y_test)))
    
      #defining parameters for logistic regression
    params = {
        'C': [0.1, 0.5, 1, 5, 10, 50, 100],
        'solver': ['liblinear']
    }
    grid_thing = GridSearchCV(LogisticRegression(), params, n_jobs = 1)
    grid_thing.fit(x_train, y_train)
    fil_out.write("%s, %0.2f, %0.2f\n"%('logistic', grid_thing.best_score_, grid_thing.score(x_test, y_test)))
    
      #defining parameters for k-nearest
    params = {
        'n_neighbors': range(1, 51),
        'leaf_size': range(5, 65, 5),
        'algorithm': ['auto']
    }
    grid_thing = GridSearchCV(KNeighborsClassifier(), params, n_jobs = 1)
    grid_thing.fit(x_train, y_train)
    fil_out.write("%s, %0.2f, %0.2f\n"%('knn', grid_thing.best_score_, grid_thing.score(x_test, y_test)))
    
      #defining parameters for DecisionTree
    params = {
        'max_depth': range(1, 51),
        'min_samples_split': range(2, 11)
    }
    grid_thing = GridSearchCV(DecisionTreeClassifier(), params, n_jobs = 1)
    grid_thing.fit(x_train, y_train)
    fil_out.write("%s, %0.2f, %0.2f\n"%('decision_tree', grid_thing.best_score_, grid_thing.score(x_test, y_test)))
    
      #defining parameters for RandomForest
    params = {
        'max_depth': range(1, 51),
        'min_samples_split': range(2, 11)
    }
    grid_thing = GridSearchCV(RandomForestClassifier(), params, n_jobs = 1)
    grid_thing.fit(x_train, y_train)
    fil_out.write("%s, %0.2f, %0.2f\n"%('random_forest', grid_thing.best_score_, grid_thing.score(x_test, y_test)))

#final step
if __name__ == "__main__":
    parser = argP.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    if args and args.input_file and args.output_file:
        main(args.input_file, args.output_file)