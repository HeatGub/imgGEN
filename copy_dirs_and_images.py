import os
from pathlib import Path
import shutil
import time
import database

def copy_dirs_and_images(src: Path, dest: Path, exclude=None):
    start_time = time.time()
    src = Path(src).resolve()
    dest = Path(dest).resolve()
    exclude = set(exclude or [])
    dirs_copied = 0
    imgs_copied = 0

    for item in src.rglob("*"):
        # Skip excluded folders
        if any(part in exclude for part in item.parts):
            continue

        # Compute relative path and destination path
        relative = item.relative_to(src)
        target_path = dest / relative

        if item.is_dir():
            target_path.mkdir(parents=True, exist_ok=True)  # Create folders - IDEMPOTENCY with parents=True
            dirs_copied +=1
        elif item.is_file():
            target_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure folder exists
            shutil.copy2(item, target_path)  # Copy with metadata
            imgs_copied +=1
    
    print(f"COPIED\n{dirs_copied} folders \n{imgs_copied} images in {round(time.time() - start_time, 1)} seconds")

# copy_dirs_and_images("D:/imgGEN/paths/create/samples", "D:/imgGEN/paths/create/generated", exclude=[])

# ___________________________________________EXCLUDE FINAL___________________________________________
def walk_with_pathlib(root_path, exclude=None):
    root_path = Path(root_path)
    exclude = set(exclude or [])
    output = []

    # .rglob DOES NOT GUARANTEE THE SAME WALKING ORDER (SORT FIRST IF NEEDED)
    for item in sorted(root_path.rglob("*.webp")): # sorted
    # for item in root_path.rglob("*"): # * matches files and dirs
        # Check if any parent directory matches exclusion
        if any(part in exclude for part in item.parts):
            continue

        if item.is_dir():
            print(f"📁 Folder: {item}")
        elif item.is_file():
            print(f"\t📄 File: {item}")
            output.append({"dir": str(item.parent), "file_name": f"{item.stem}{item.suffix}"})
            # print(f"\t📄 File: {item.stem}{item.suffix}")
            # print(f"\t📄 File: {item.parent}") # its dir
    print(output)
    database.create_table_if_necessary()
    database.insert_many(output)

walk_with_pathlib("D:/imgGEN/paths/create", exclude=["venv", "main.py"])



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
# target_path.parent.mkdir(parents=True, exist_ok=True)
# All missing parent directories are created recursively!!! (parents=True)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT



# ___________________________________________EXCLUDE___________________________________________
# def walk_with_pathlib(root_path, exclude=None):
#     root_path = Path(root_path)
#     exclude = set(exclude or [])

#     for item in root_path.rglob("*"):

#         # Check if any parent directory matches exclusion
#         if any(part in exclude for part in item.parts):
#             continue
#         # else:
#             # print(item.parts)
#             # 📁 Folder: D:\imgGEN\paths\original\3
#             # ('D:\\', 'imgGEN', 'paths', 'original', '2', '2a')

#         if item.is_dir():
#             print(f"📁 Folder: {item}")
#         elif item.is_file():
#             print(f"\t📄 File: {item}")

# walk_with_pathlib("D:/imgGEN/paths", exclude=["venv"])

# print("\n\t\tos\n")

# def walk_with_os(root_path, exclude=None):
#     exclude = set(exclude or [])

#     for root, dirs, files in os.walk(root_path):
#         # Filter excluded directories *in-place*
#         dirs[:] = [d for d in dirs if d not in exclude]

#         print(f"📁 Folder: {root}")
#         for file in files:
#             print(f"\t📄 File: {os.path.join(root, file)}")

# walk_with_os("D:/imgGEN/paths", exclude=["venv"])


# ___________________________________________BASIC___________________________________________
# PATH = r"D:\imgGEN\paths"

# for root, dirs, files in os.walk(PATH):
#     print(f"Current folder: {root}")
#     for d in dirs:
#         print(f"  Sub-folder: {os.path.join(root, d)}")
#     # for f in files:
#     #     print(f"  File: {os.path.join(root, f)}")

# print('\npathlib\n')


# def walk_path(path: Path):
#     for item in path.rglob("*"):
#         if item.is_dir():
#             print(f"Directory: {item}")
#         # elif item.is_file():
#         #     print(f"  File: {item}")

# walk_path(Path(PATH))
