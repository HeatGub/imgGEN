import os
import random
import time
from PIL import Image
import shutil

start_time = time.time()

def create_folders_with_images(n, base_path="./create/samples"):
    images_created = 0
    dirs_created = 0
    subdirs_created = 0
    # Determine number of digits needed for zero-padding
    # padding = len(str(n))
    padding = 6

    for i in range(1, n+1):
        parent_name = str(i).zfill(padding)
        parent_path = os.path.join(base_path, parent_name)
        os.makedirs(parent_path, exist_ok=True) # 000001 - n
        dirs_created += 1

        def create_subdir():
            nonlocal images_created # otherwise out of scope
            nonlocal dirs_created
            random_digits = ''.join(random.choices("0123456789", k=9))
            subfolder_name = f"{parent_name}{random_digits}"
            subfolder_path = os.path.join(parent_path, subfolder_name)
            os.makedirs(subfolder_path, exist_ok=True)
            dirs_created += 1

            def create_image():
                img_path = os.path.join(subfolder_path, "tiny.webp")
                image = Image.new("RGB", (4, 4), color=(0, 128, 255))  # Small blue square
                image.save(img_path, "WEBP", quality=1)

            # CREATE IMAGE
            if random.random() < 0.95:
                create_image()
                # print(images_created)
                images_created +=1
            
        # ALWAYS CREATE 1 DIR
        create_subdir()
        subdirs_created += 1

        # ADDITIONAL DIRS
        while random.random() < 0.25:
            create_subdir()
            subdirs_created += 1

    return dirs_created, images_created, subdirs_created

def cleanup_dirs():
    if os.path.exists("./create/samples"):
        shutil.rmtree('./create/samples') # remove old samples
    if os.path.exists("./create/generated"):
        shutil.rmtree('./create/generated') # remove old generated

if __name__ == "__main__":
    cleanup_dirs()
    n_base_folders = 100
    dirs_n, images_n, subdirs_n = create_folders_with_images(n=n_base_folders)
    print(f"MADE \n{dirs_n} folders ({subdirs_n} subdirs)\n{images_n} images\nin {round(time.time() - start_time, 1)} seconds")
