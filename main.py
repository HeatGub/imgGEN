from pathlib import Path
import time
import database
import traceback # trace = traceback.format_exc() - formats for safe db saving
# from PIL import Image
import logging
import config
import base64
from openai import OpenAI, OpenAIError
import random
import logger_setup

logger_setup.setup_logging()
logger = logging.getLogger(__name__)

ERROR_COUNTER = 0

class RetryableError(Exception):
    """Raised when action can be retried safely."""
    pass

class NonRetryableError(Exception):
    """Raised for non-retriable internal issues (I/O, decoding, etc)."""
    pass

def call_openai_api_and_save_image(openai_client, original_image_dir, original_file_name):
    start_time = time.time()
    logger.info(f"Generating {original_image_dir}/{original_file_name}")
    original_image_dir = Path(original_image_dir)
    original_image_path = original_image_dir / original_file_name
    new_dir = original_image_dir / "converted"
    file_name_without_extension = Path(original_file_name).stem
    new_file_name = f"{file_name_without_extension}-converted_1024_1024.png"
    new_full_path = new_dir / new_file_name

    new_dir.mkdir(parents=True, exist_ok=True) # parents=True - if any or all parent folders are missing they are created recursively

    client = openai_client

    try:
        with open(original_image_path, "rb") as original_image:
            openai_response = client.images.edit(
                model = "gpt-image-1",
                image = [original_image],
                prompt = config.OPENAI_PROMPT,
                quality = "medium",
                output_format = config.OUTPUT_IMAGE_EXTENSION,
                size = "1024x1024",
                # output_compression = 50,
            )
    except OpenAIError as e:
        raise RetryableError(f"OpenAI API error: {e}") from e
    except Exception as e:
        raise NonRetryableError(f"Failed to call OpenAI API: {e}") from e

    try:
        image_base64 = openai_response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        with open(new_full_path, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        raise NonRetryableError(f"Failed to decode or save image: {e}") from e

    elapsed_time = time.time() - start_time
    logger.info(f"Generated {new_full_path} in {elapsed_time:.1f} seconds")


def convert_single_pending_image(openai_client):
    global ERROR_COUNTER
    id = dir = file_name = None  # prevent NameError in except block
    try:
        result = database.get_single_pending_set_status_processing()
        if result is None:
            return False  # No pending image

        id, dir, file_name = result

        last_exception = None
        for attempt in range(config.OPENAI_CALLS_MAX_RETRIES +1):
            try:
                call_openai_api_and_save_image(openai_client, dir, file_name)
                database.set_status_processed(id)
                ERROR_COUNTER = 0
                return True
            except RetryableError as e:
                last_exception = e
                logger.warning(f"Retryable error (attempt {attempt + 1}/{config.OPENAI_CALLS_MAX_RETRIES + 1}) during processing of image {file_name} (ID: {id}): {e}", exc_info=False)
                time.sleep(2 ** attempt) # exponential wait until next call
            except NonRetryableError as e:
                database.set_status_error(id, 'processing_error', e)
                logger.error(f"Failed to process image {file_name} (ID: {id}): {e}", exc_info=False)
                ERROR_COUNTER += 1
                break
            except Exception as e:
                database.set_status_error(id, 'processing_error', e)
                logger.critical(f"Failed to process image {file_name} (ID: {id}): {e}", exc_info=False)
                ERROR_COUNTER += 1
                break
        else: # If all retries fail (i.e., BREAK IS NEVER HIT), then else runs → raises the final failure
            logger.error(f"Failed to process image {file_name} (ID: {id}): {last_exception}", exc_info=False)  # all attempts failed
            database.set_status_error(id, 'processing_error', last_exception)
            ERROR_COUNTER += 1
            return True # continue with next img
            
    except Exception as e:
        if id is not None:
            database.set_status_error(id, 'processing_error', e)
        if id and file_name:
            logger.error(f"Failed to process image {file_name} (ID: {id}): {e}", exc_info=False)
        else:
            logger.critical(f"Error during image processing: {e}", exc_info=True)
        ERROR_COUNTER += 1
        return True  # continue processing others

def process_all_pending_images():
    openai_client = OpenAI(api_key=config.OPENAI_API_KEY, timeout=config.OPENAI_TIMEOUT_SECONDS)
    while True:
        keep_going = convert_single_pending_image(openai_client)
        if ERROR_COUNTER >= config.ERROR_COUNTER_LIMIT:
            logger.critical(f"ERROR_COUNTER LIMIT HIT: {ERROR_COUNTER}")
            # sendEmail()
            break
        if keep_going == False:
            logger.info("No more pending images")
            # sendEmail()
            break  # EXIT LOOP IF NO MORE PENDINGS

if __name__ == "__main__":
    process_all_pending_images()
    # print(database.get_single_pending_set_status_processing())


# TODO
# timeouty poustawiać dla api


# PYTANIA 1
# ile kompow/procesow ma generowac obrazki
# czy obrazki sciagamy w 1 duzym zipie czy pojedynczo
# gdzie uploadujemy i tez czy w bulku czy pojedynczo
# zapisujemy w tym samym miejscu, ale z inną nazwą? Usuwamy oryginał?


# NOTES:
# overwrites image if processed 2nd time