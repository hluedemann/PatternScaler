import argparse
import string
import os
from PIL import Image
from tqdm import tqdm


def get_argument_parser():

    parser = argparse.ArgumentParser(description="Options for Pattern Scaler")
    parser.add_argument('-f', '--folder', required=True,
                        help='root folder of the patterns')

    return parser

def prepare_output_folders(root_dir: string) -> list:

    pattern_name = root_dir.split("/")[-1]
    dir = os.path.join(root_dir, pattern_name)
    dir_jpg = os.path.join(dir, "JPG")
    dir_png = os.path.join(dir, "PNG")
    dir_2x2 = os.path.join(dir, "2x2")
    os.makedirs(dir_jpg)
    os.makedirs(dir_png)
    os.makedirs(dir_2x2)

    return [dir_jpg, dir_png, dir_2x2]

def get_images(root_dir: string) -> list:

    dir = os.path.join(root_dir, "Upscaled")
    images = list()

    try:
        for img_path in os.listdir(dir):
            image = Image.open(os.path.join(dir, img_path))
            images.append(image)
    except:
        raise FileNotFoundError(f"The folder {dir} could not be opend!")

    return images

def process_images(root_dir: string) -> None:

    save_dirs = prepare_output_folders(root_dir)

    images = get_images(root_dir)

    for i, img in tqdm(enumerate(images), total=len(images)):
        new_img = img.convert("RGB").resize((3600, 3600), Image.BICUBIC)
        new_img.save(os.path.join(save_dirs[0], f"pattern_{str(i+1).zfill(2)}.jpg"),
                     quality=100,
                     subsampling=0)
        new_img.save(os.path.join(
            save_dirs[1], f"pattern_{str(i+1).zfill(2)}.png"))

        large_img = Image.new("RGB", (7200, 7200))
        large_img.paste(new_img, (0, 0))
        large_img.paste(new_img, (0, 3600))
        large_img.paste(new_img, (3600, 0))
        large_img.paste(new_img, (3600, 3600))
        large_img.save(os.path.join(save_dirs[2], f"pattern_2x2_{str(i+1).zfill(2)}.jpg"),
                       quality=95,
                       subsampling=0)


if __name__ == "__main__":

    parser = get_argument_parser()
    args = parser.parse_args()
    root_dir = args.folder

    process_images(root_dir)
