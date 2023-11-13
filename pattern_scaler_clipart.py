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
    w_dir_jpg = os.path.join(dir, "JPG", "White_Backgound")
    b_dir_jpg = os.path.join(dir, "JPG", "Black_Backgound")
    w_dir_png = os.path.join(dir, "PNG", "White_Background")
    b_dir_png = os.path.join(dir, "PNG", "Black_Background")
    t_dir_png = os.path.join(dir, "PNG", "Transparent_Background")
    w_dir_2x2_JPG = os.path.join(dir, "2x2_JPG", "White_Backgound")
    b_dir_2x2_JPG = os.path.join(dir, "2x2_JPG", "Black_Background")
    w_dir_2x2_PNG = os.path.join(dir, "2x2_PNG", "White_Backgound")
    b_dir_2x2_PNG = os.path.join(dir, "2x2_PNG", "Black_Background")
    t_dir_2x2_PNG = os.path.join(dir, "2x2_PNG", "Transparent_Background")

    os.makedirs(w_dir_jpg)
    os.makedirs(b_dir_jpg)
    os.makedirs(w_dir_png)
    os.makedirs(b_dir_png)
    os.makedirs(t_dir_png)
    os.makedirs(w_dir_2x2_JPG)
    os.makedirs(b_dir_2x2_JPG)
    os.makedirs(w_dir_2x2_PNG)
    os.makedirs(b_dir_2x2_PNG)
    os.makedirs(t_dir_2x2_PNG)

    return [w_dir_jpg, b_dir_jpg, w_dir_png, b_dir_png, t_dir_png, w_dir_2x2_JPG, b_dir_2x2_JPG, w_dir_2x2_PNG, b_dir_2x2_PNG, t_dir_2x2_PNG]


def get_images(root_dir: string) -> list:

    dir = os.path.join(root_dir, "Patterns")
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
        
        #Transparent

        img.save(os.path.join(save_dirs[4], f"pattern_transparent_{str(i+1).zfill(2)}.png"))

        large_img = Image.new("RGBA", (7200, 7200))
        large_img.paste(img, (0, 0))
        large_img.paste(img, (0, 3600))
        large_img.paste(img, (3600, 0))
        large_img.paste(img, (3600, 3600))
        large_img.save(os.path.join(save_dirs[9], f"pattern_transparent_2x2_{str(i+1).zfill(2)}.png"))

        # White

        new_image = Image.new("RGBA", img.size, "WHITE")
        new_image.paste(img, mask=img)
        new_image = new_image.convert("RGB")

        large_img = Image.new("RGB", (7200, 7200))
        large_img.paste(new_image, (0, 0))
        large_img.paste(new_image, (0, 3600))
        large_img.paste(new_image, (3600, 0))
        large_img.paste(new_image, (3600, 3600))
        large_img.save(os.path.join(save_dirs[7], f"pattern_white_{str(i+1).zfill(2)}.png"))
        large_img.save(os.path.join(save_dirs[5], f"pattern_white_{str(i+1).zfill(2)}.jpg"), quality=95, subsampling=0)
        

        new_image.save(os.path.join(save_dirs[0], f"pattern_white_{str(i+1).zfill(2)}.png"))
        new_image.save(os.path.join(save_dirs[2], f"pattern_white_{str(i+1).zfill(2)}.jpg"), quality=100, subsampling=0)

        ## Black

        new_image = Image.new("RGBA", img.size, "BLACK")
        new_image.paste(img, mask=img)
        new_image = new_image.convert("RGB")

        new_image.save(os.path.join(save_dirs[1], f"pattern_black_{str(i+1).zfill(2)}.png"))
        new_image.save(os.path.join(save_dirs[3], f"pattern_black_{str(i+1).zfill(2)}.jpg"), quality=100, subsampling=0)

                
        large_img = Image.new("RGB", (7200, 7200))
        large_img.paste(new_image, (0, 0))
        large_img.paste(new_image, (0, 3600))
        large_img.paste(new_image, (3600, 0))
        large_img.paste(new_image, (3600, 3600))
        large_img.save(os.path.join(save_dirs[8], f"pattern_black_{str(i+1).zfill(2)}.png"))
        large_img.save(os.path.join(save_dirs[6], f"pattern_black_{str(i+1).zfill(2)}.jpg"), quality=95, subsampling=0)



if __name__ == "__main__":

    parser = get_argument_parser()
    args = parser.parse_args()
    root_dir = args.folder

    process_images(root_dir)
