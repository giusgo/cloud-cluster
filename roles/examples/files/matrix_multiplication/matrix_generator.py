import numpy as np

def generate_and_save_matrix(n, m, filename):
    # Generar una matriz aleatoria de tamaño n x m
    matrix = np.random.rand(n, m)
    # Guardar la matriz en un archivo
    np.savetxt(filename, matrix)

def main():
    n = int(input("Enter the number of rows for the first matrix: "))
    m = int(input("Enter the number of columns for the first matrix (and rows for the second): "))
    p = int(input("Enter the number of columns for the second matrix: "))

    # Generar y guardar las dos matrices
    generate_and_save_matrix(n, m, "matrix_A.txt")
    generate_and_save_matrix(m, p, "matrix_B.txt")

if __name__ == "__main__":
    main()

