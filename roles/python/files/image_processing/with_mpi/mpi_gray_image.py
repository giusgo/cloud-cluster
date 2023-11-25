from mpi4py import MPI
from PIL import Image
import time

def convert_to_gray(image_path):
    with Image.open(image_path) as image:
        gray_image = image.convert("L")
        gray_image.save(f'mpi_processed_{image_path}')

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    images = ["image_0.jpg", "image_1.jpg", "image_2.jpg"]

    # Inicia el tiempo total
    start_time = MPI.Wtime() if rank == 0 else None

    if rank < len(images):
        node_start_time = MPI.Wtime()
        convert_to_gray(images[rank])
        node_end_time = MPI.Wtime()
        print(f"Node {rank} processed {images[rank]} in {node_end_time - node_start_time} seconds.")
    else:
        print(f"Node {rank} didn't processed any image.")

    # Recolecta los tiempos finales de cada nodo
    end_times = comm.gather(MPI.Wtime(), root=0)

    # Calcula y muestra el tiempo total en el nodo principal
    if rank == 0:
        total_time = max(end_times) - start_time
        print(f"\nTotal execution time: {total_time} seconds.")

if __name__ == "__main__":
    main()

