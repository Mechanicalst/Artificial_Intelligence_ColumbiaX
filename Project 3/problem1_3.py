#importing libraries
import numpy as np
from matplotlib import pyplot as plt
import argparse as argP

#Creating classes and defintions
class Percept:
    def __init__(self, labels: np.array):
        self.weights = np.zeros(3)
        self.labels = labels

    def pred_func(self, row: np.array):
        pred_func = np.dot(row, self.weights)
        if pred_func > 0:
            return 1
        else:
            return -1
        
    def func_results(self, data: np.array):
        correct, incorrect = 0, 0
        for (row, actual) in zip(data, self.labels):
            pred_func = self.pred_func(row)
            if actual != pred_func:
                incorrect += 1
            else:
                correct += 1
        return correct, incorrect

    def func_train(self, data):
        for (row, label) in zip(data, self.labels):
            actual = label
            pred_func = self.pred_func(row)
            if actual < pred_func:
                self.weights -= row
            elif actual > pred_func:
                self.weights += row

        correct, incorrect = self.func_results(data)
        return self.weights, correct, incorrect

#defining the graph function
def graph_func(data: np.array, perceptron: Percept):
    colormap = np.array(['r', 'k'])
    xZi = [0 if x == 1 else 1 for x in perceptron.labels]
    Xz = data[:, [0]]
    yz = data[:, [1]]
    plt.scatter(Xz.flatten(), yz.flatten(), c=colormap[xZi])
    weight_W = perceptron.weights
    x2 = np.linspace(min(Xz), max(Xz))
    QR = -weight_W[0] / weight_W[1]
    y2 = QR * x2 - (weight_W[2]) / weight_W[1]
    plt.plot(x2, y2, 'k-')
    plt.savefig('figure1')

#defining the main function
def main(input_file, output_file):
    fi = open(input_file, 'rb')
    raw_data = np.loadtxt(fi, delimiter=',')
    rows = raw_data.shape[0]
    labels = raw_data[:, [-1]].flatten()
    data = raw_data[:, [0, 1]]
    const = np.ones(rows)
    const.shape = (rows, 1)
    data = np.hstack((data, const))
    
    #creating the percptron using the percept labels
    perceptron = Percept(labels)

    incorrect = 1
    
    #writing into the output file
    fo = open(output_file, 'w')

    while incorrect:
        weights, correct, incorrect = perceptron.func_train(data)
        fo.write("%d, %d, %d\n"%(weights[0], weights[1], weights[2]))

    graph_func(data, perceptron)


if __name__ == "__main__":
    parser = argP.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    if args and args.input_file and args.output_file:
        main(args.input_file, args.output_file)

#end of project






