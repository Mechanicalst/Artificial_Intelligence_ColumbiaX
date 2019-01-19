#importing libraries

from statistics import stdev
from statistics import mean
import argparse as argP
import numpy as np

#Linear regression being performed utilizing gradient descent
def gradient_descent(L, m, alpha, Iter):
    Wght = np.zeros(L.shape[1])
    feat = L.shape[1]
    n = len(m)
    sse = []

    for each in range(Iter):
        y_est = np.dot(L, Wght)
        error = y_est - m
        sse = np.sum(error ** 2)
        for i in range(feat):
            errors_x = error * L[:,i]
            Wght[i] -= alpha * (1/n) * np.sum(errors_x)
#  one at a time, the weights are being picked
    return alpha, Iter, Wght[0], Wght[1], Wght[2], sse   



# z-scores are being returned
def feature_Nrm(L):
    R_mean = []
    R_std = []
    Norm_x = L
    feat = L.shape[1]
    for f in range(feat):
        m = mean(L[:, f])
        s = stdev(L[:, f])
        R_mean.append(m)
        R_std.append(s)
        Norm_x[:, f] = (Norm_x[:, f] - m) / s

    return Norm_x


# right till the SSE begins to increase it continues to execute
def find__alpha(L, m, Iter):
    alpha_q = 0.00
    test_alpha_q = 0.00
    SSE = float('Inf')
    while True:
        result = gradient_descent(L, m, test_alpha_q, Iter)
        test_alpha_q+=0.01
        SSE_new = result[-1]
        if SSE_new > SSE:
            break

        SSE = SSE_new
        alpha_q = test_alpha_q

    return round(alpha_q, 2)


def main(input_file, output_file):
    # vals being 
    alpha_s = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    Iter = 100

    # input output for file
    fil_in = open(input_file, 'rb')
    fil_out = open(output_file, 'w')
    raw_Dt = np.loadtxt(fil_in, delimiter=',')

    # data being Normalized and also matrix being built for regression
    X_Nrm = feature_Nrm(raw_Dt[:, :-1])
    b_0 = np.ones(X_Nrm.shape[0])
    L = np.column_stack((b_0.T,X_Nrm))
    m = raw_Dt[:, -1]

   
    alpha_q = 0.62
    alpha_s.append(alpha_q)

    # perform gradient decent on weights for each alpha
    for alpha in alpha_s:
        result = gradient_descent(L, m, alpha, Iter)
        fil_out.write("%s, %d, %s, %s, %s\n" % result[:-1])

if __name__ == "__main__":
    parser = argP.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    if args and args.input_file and args.output_file:
        main(args.input_file, args.output_file)
