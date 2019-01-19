#Importing the libraries
import matplotlib.pyplot as plt
import sys
import numpy as np

#Defining 
def f(q):
    return 1 if q > 0 else -1

def draw(L, m, n):
   # decision boundary and misclassification representation

    for z in range(L.shape[0]):
        if m[z] == 1:
            plt.plot(L[z, 0], L[z, 1], 'ro')
        else:
            plt.plot(L[z, 0], L[z, 1], 'bx')
    
    Min_x = L.min(axis=0)
    Max_x = L.max(axis=0)
    
    x2 = [Min_x[0] - 1, Max_x[0] + 1]
    y2 = -(n[2] + n[0]*x2)/n[1]
    plt.plot(x2, y2, 'k')
    plt.axis([Min_x[0] - 1, Max_x[0] + 1, Min_x[1] - 1, Max_x[1] + 1])    
    plt.show()

def PLA(L, m, output_file, animate = False):
    
    #Perceptron Learning Algorithm (PLA with weights)

    B = L.shape[1]
    n = np.zeros((B + 1, 1))
    conv = False

    open(output_file, 'w').close()
    while not conv:
        conv = True
        for z in range(L.shape[0]):
            if m[z]*f(n[-1] + np.dot(L[[z], :], n[:-1, [0]])) <= 0:
                n[-1] = n[-1] + m[z]
                n[:-1, [0]] = n[:-1, [0]] + m[z]*np.transpose(L[[z], :])
                conv = False

        if animate:
            draw(L, m, n)
    
        with open(output_file, "a") as text_file:
            for fi in n:
                if fi[0].is_integer():
                    text_file.write(str(int(fi[0])) + ",")
                else:
                    text_file.write(str(fi[0]) + ",")
            text_file.write("\n")

    return n

    dataset = np.genfromtxt(sys.argv[1], delimiter =',', skip_header = 0, names = None)

    L = dataset[:, [0, 1]]
    m = dataset[:, [2]]

    # For thhe case of Visualizing and debugging decision-boundary
    n = PLA(L, m, sys.argv[2], False)
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ('Usage: python <input.csv> <output.csv>')
        sys.exit()


