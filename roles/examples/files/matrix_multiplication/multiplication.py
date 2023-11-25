import numpy as np
import time

def multiply_matrices(A, B):
    return np.dot(A, B)

def main():
    # Leer las matrices desde los archivos
    A = np.loadtxt("matrix_A.txt")
    B = np.loadtxt("matrix_B.txt")

    start_time = time.time()
    
    # Multiplicación de matrices
    C = multiply_matrices(A, B)

    end_time = time.time()

    print("Resultant Matrix:\n", C)
    print("Total Time: {:.6f} seconds".format(end_time - start_time))

if __name__ == "__main__":
    main()

