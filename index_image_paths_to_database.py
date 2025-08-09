from pathlib import Path
import time
import database
import traceback
import logging
import config
import logger_setup

logger_setup.setup_logging()
logger = logging.getLogger(__name__)

def scan_paths_and_index_images(root_dir, exclude = None):
    try:
        start_time = time.time()
        root_dir = Path(root_dir)
        exclude = set(exclude or [])
        images_found_list = []

        # rglob does not guarantee the same walking order (sort first if needed)
        image_paths = (
            item for item in root_dir.rglob("*") # global search of any item (dir/file)
            if item.suffix.lower() in config.ALLOWED_INPUT_IMAGE_EXTENSIONS # include only allowed extensions
        )

        for item in image_paths:
            # print(f"{item.stem}{item.suffix}")
            images_found_list.append({"dir": str(item.parent), "file_name": f"{item.stem}{item.suffix}"})
        
        message = f"Image paths scanned in {round(time.time() - start_time, 1)}s"
        print(message)
        logger.info(message)
        database.create_table_if_necessary()
        database.insert_many(images_found_list)
        database.select_all()
    except Exception: # does not catch system-exiting exceptions
        traceback.print_exc()
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    scan_paths_and_index_images(config.ROOT_DIR, exclude=["venv", "main.py"])