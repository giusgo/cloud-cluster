from mpi4py import MPI
import numpy as np
import time

def parallel_matrix_multiply(A, B, comm, rank, size):
    # Calculamos cuántas filas enviar a cada proceso
    num_rows_A = A.shape[0]
    rows_per_process = num_rows_A // size
    remainder = num_rows_A % size

    # Determinar el número de filas que tendrá cada proceso
    send_counts = [(rows_per_process + 1) * A.shape[1] if i < remainder else rows_per_process * A.shape[1] for i in range(size)]
    displacements = [sum(send_counts[:i]) for i in range(size)]

    # Crear buffer para las filas locales de A en cada proceso
    local_A_size = (rows_per_process + 1) if rank < remainder else rows_per_process
    local_A = np.zeros((local_A_size, A.shape[1]), dtype=A.dtype)

    # Distribuir las filas de A a todos los procesos
    comm.Scatterv([A, send_counts, displacements, MPI.DOUBLE], local_A, root=0)

    # Transmitir B a todos los procesos
    comm.Bcast(B, root=0)

    # Multiplicar localmente
    local_C = np.dot(local_A, B)

    # Preparar para recolectar los resultados en el proceso raíz
    all_C = None
    if rank == 0:
        all_C = np.zeros((num_rows_A, B.shape[1]), dtype=A.dtype)

    # Determinar la cantidad de datos a recibir de cada proceso
    recv_counts = [count // A.shape[1] * B.shape[1] for count in send_counts]
    displacements = [sum(recv_counts[:i]) for i in range(size)]

    # Recolectar los resultados parciales en el proceso raíz
    comm.Gatherv(local_C, [all_C, recv_counts, displacements, MPI.DOUBLE], root=0)

    return all_C

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    A, B = None, None
    if rank == 0:
        # Leer las matrices desde archivos
        A = np.loadtxt("matrix_A.txt")
        B = np.loadtxt("matrix_B.txt")

    # Obtenemos las dimensiones de A y B
        dimensions = A.shape, B.shape
    else:
        A, B = None, None
        dimensions = None

    # Transmitir las dimensiones a todos los procesos
    dimensions = comm.bcast(dimensions, root=0)

    # Todos los procesos, excepto el raíz, inicializan A y B basándose en las dimensiones recibidas
    if rank != 0:
        A = np.empty(dimensions[0], dtype=np.float64)
        B = np.empty(dimensions[1], dtype=np.float64)

    start_time = MPI.Wtime()

    # Multiplicación de matrices en paralelo
    C = parallel_matrix_multiply(A, B, comm, rank, comm.Get_size())

    end_time = MPI.Wtime()

    if rank == 0:
        print("Resultant Matrix:\n", C)
        print("Total Time: {:.6f} seconds".format(end_time - start_time))

if __name__ == "__main__":
    main()

