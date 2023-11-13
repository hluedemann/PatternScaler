import argparse
import string
import os
from PIL import Image
from tqdm import tqdm
import random


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
    os.makedirs(dir_png)
    os.makedirs(dir_2x2)

    return [dir_jpg, dir_png, dir_2x2]


def get_images(root_dir: string) -> list:

    images_paths = sorted([f for f in os.listdir(root_dir) if f.endswith(".png") or 
                    f.endswith(".jpg")])
    images = [Image.open(os.path.join(root_dir, path)) for path in images_paths]

    return images_paths, images



def split_img_horizontal(img):

    width, height = img.size

    rand_num = random.randint(width // 4, width-width // 4)

    box_top = (0, 0, width, rand_num)
    crop_top = img.crop(box_top)
    box_bottom = (0, rand_num, width, height)
    crop_bottom = img.crop(box_bottom)


    cropped_img_top = Image.new("RGBA", (width, rand_num))
    cropped_img_bottom = Image.new("RGBA", (width, height-rand_num))

    cropped_img_top.paste(crop_top, (0, 0))
    cropped_img_bottom.paste(crop_bottom, (0, 0))

    return cropped_img_top, cropped_img_bottom

def split_img_vert(img):

    width, height = img.size

    rand_num = random.randint(width // 4, width-width // 4)

    box_left = (0, 0, rand_num, height)
    crop_left = img.crop(box_left)
    print("left", crop_left)
    box_right = (rand_num, 0, height, height)
    crop_right = img.crop(box_right)
    print("right", crop_right)


    cropped_img_left = Image.new("RGBA", (rand_num, height))
    cropped_img_right = Image.new("RGBA", (width-rand_num, height))

    cropped_img_left.paste(crop_left, (0, 0))
    cropped_img_right.paste(crop_right, (0, 0))

    return cropped_img_left, cropped_img_right



def process_images(root_dir: string) -> None:
    
    os.makedirs(os.path.join(root_dir, "Split"), exist_ok=True)

    images_paths, images = get_images(root_dir)
    
    variations = 1

    for img_path, img in tqdm(zip(images_paths, images), total=len(images)):

        clipart_name = img_path.split("/")[-1].split(".")[0]
        clipart_folder = os.path.join(root_dir, "Split", clipart_name)
        os.makedirs(clipart_folder, exist_ok=True)


        for i in range(1, 4 * variations, 4):
        
            cropped_img_left, cropped_img_right = split_img_vert(img)
            cropped_img_top, cropped_img_bottom = split_img_horizontal(img)

            cropped_img_left.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i).zfill(4)}_1.png"))
            cropped_img_right.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i).zfill(4)}_2.png"))

            cropped_img_top.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i+1).zfill(4)}_1.png"))
            cropped_img_bottom.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i+1).zfill(4)}_2.png"))

            rand_num = random.randint(0, 360)
            rot_img = img.rotate(rand_num)
            cropped_img_left, cropped_img_right = split_img_vert(rot_img)

            rand_num = random.randint(0, 360)
            rot_img = img.rotate(rand_num)
            cropped_img_top, cropped_img_bottom = split_img_horizontal(rot_img)

            cropped_img_left.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i+2).zfill(4)}_1.png"))
            cropped_img_right.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i+2).zfill(4)}_2.png"))

            cropped_img_top.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i+3).zfill(4)}_1.png"))
            cropped_img_bottom.save(os.path.join(clipart_folder, f"{clipart_name}_split_{str(i+3).zfill(4)}_2.png"))



if __name__ == "__main__":

    parser = get_argument_parser()
    args = parser.parse_args()
    root_dir = args.folder

    process_images(root_dir)
