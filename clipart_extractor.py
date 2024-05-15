import argparse
import os
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager


def get_argument_parser():

    parser = argparse.ArgumentParser(description="Options for Pattern Scaler")
    parser.add_argument('-f', '--folder', required=True,
                        help='root folder of the patterns')

    return parser

def prepare_output_folders(root_dir, img_iter):

    dir = os.path.join(root_dir, "Extracted", f"image_{img_iter}".zfill(3))
    os.makedirs(dir, exist_ok=True)

    return dir


def get_images(root_dir) -> list:

    dir = os.path.join(root_dir, "Background_Removed")
    images = list()

    try:
        for img_path in os.listdir(dir):
            image = Image.open(os.path.join(dir, img_path))
            images.append(image)
    except:
        raise FileNotFoundError(f"The folder {dir} could not be opend!")

    return images

def find_starting_point(image):

    width, height = image.size

    for y in range(height):
        for x in range(width):
            color = image.getpixel((x, y))
            if color != (0, 0, 0, 0):
                return (x, y)
            
    return None

def find_clipart_area(image, start_point):

    width, height = image.size
    result = dict()
    stack = [start_point]

    while stack:
        x, y = stack.pop()
        pixel_value = image.getpixel((x, y))

        if pixel_value != (0, 0, 0, 0):
            result[(x, y)] = pixel_value

            image.putpixel((x, y), (0, 0, 0, 0))

            neighbors = [
                (x, y - 1),  # top
                (x, y + 1),  # bottom
                (x - 1, y),  # left
                (x + 1, y)   # right
            ]

            for neighbor in neighbors:
                nx, ny = neighbor
                if 0 <= nx < width and 0 <= ny < height:  # Check if neighbor is within image boundaries
                    stack.append(neighbor)

    return result

def is_clipart(result):
    if len(result) < 1000:
        return False
    else:
        return True

def save_clipart(result, root_dir, iter):
    x_values, y_values = zip(*result.keys())
    left, upper, right, lower = min(x_values), min(y_values), max(x_values), max(y_values)
    width = right - left + 1
    height = lower - upper + 1

    new_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    for position, rgba in result.items():
        x, y = position
        new_image.putpixel((x - left, y - upper), rgba)

    out_path = os.path.join(root_dir, str(iter).zfill(4) + ".png")
    new_image.save(out_path)

def process_image(image_path, save_dir, iter_clipart, lock):
    image = Image.open(image_path)
    
    while True:
        start_point = find_starting_point(image)
        if start_point is None:
            break
        
        result = find_clipart_area(image, start_point)

        if is_clipart(result):
            with lock:
                current_iter_clipart = iter_clipart.value
                iter_clipart.value += 1
            save_clipart(result, save_dir, current_iter_clipart)


def process_images_parallel(root_dir, iter_clipart, lock):
    images = [os.path.join(root_dir, "Background_Removed", img_path) for img_path in os.listdir(os.path.join(root_dir, "Background_Removed"))]

    with ProcessPoolExecutor() as executor:
        futures = []
        for img_iter, image_path in enumerate(images):
            save_dir = prepare_output_folders(root_dir, img_iter)
            future = executor.submit(process_image, image_path, save_dir, iter_clipart, lock)
            futures.append(future)

        # Wait for all tasks to complete
        for future in tqdm(futures, total=len(futures)):
            future.result()

if __name__ == "__main__":
    parser = get_argument_parser()
    args = parser.parse_args()

    with Manager() as manager:
        iter_clipart = manager.Value('i', 0)
        lock = manager.Lock()
        process_images_parallel(args.folder, iter_clipart, lock)
        