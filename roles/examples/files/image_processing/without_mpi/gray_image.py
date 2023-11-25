from PIL import Image
import time

def convert_to_gray(image_path):
    with Image.open(image_path) as image:
        gray_image = image.convert("L")
        gray_image.save(f'processed_{image_path}')

def main():
    start_time = time.time()

    images = ["image_0.jpg", "image_1.jpg", "image_2.jpg"]
    for image in images:
        convert_to_gray(image)

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()

