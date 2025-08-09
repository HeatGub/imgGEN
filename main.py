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


class RetryableError(Exception):
    """Raised when action can be retried safely."""
    pass

class NonRetryableError(Exception):
    """Raised for non-retriable internal issues (I/O, decoding, etc)."""
    pass

def call_openai_api_and_save_image(original_image_dir, original_file_name):
    start_time = time.time()
    logger.info(f"Generating {original_image_dir}/{original_file_name}")
    original_image_dir = Path(original_image_dir)
    original_image_path = original_image_dir / original_file_name
    new_dir = original_image_dir / "converted"
    file_name_without_extension = Path(original_file_name).stem
    new_file_name = f"{file_name_without_extension}-converted_1024_1024.png"
    new_full_path = new_dir / new_file_name

    new_dir.mkdir(parents=True, exist_ok=True) # parents=True - if any or all parent folders are missing they are created recursively

    client = OpenAI(api_key=config.OPENAI_API_KEY, timeout=config.OPENAI_TIMEOUT_SECONDS)


    try:
        # with open(original_image_path, "rb") as original_image:
        #     openai_response = client.images.edit(
        #         model = "gpt-image-1",
        #         image = [original_image],
        #         prompt = config.OPENAI_PROMPT,
        #         quality = "low",
        #         output_format = config.OUTPUT_IMAGE_EXTENSION,
        #         size = "1024x1024",
        #         # size = "10x10",
        #         # output_compression = 50,
        #     )
        if random.random() < 0.95:
            raise RetryableError ("RETRYABLE")
        elif random.random() > 0.75:
            raise NonRetryableError ("NON-RETRYABLE")
        else:
            pass
    except OpenAIError as e:
        raise RetryableError(f"OpenAI API error: {e}") from e
    # except Exception as e: # catches raised errs from the same function
    #     raise NonRetryableError(f"Failed to call OpenAI API: {e}") from e

    try:
        image_base64 = "asdasd"
        # image_base64 = openai_response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        with open(new_full_path, "wb") as f:
            f.write(image_bytes)
    except Exception as e:
        raise NonRetryableError(f"Failed to decode or save image: {e}") from e

    elapsed_time = time.time() - start_time
    logger.info(f"Generated {new_full_path} in {elapsed_time:.1f} seconds")


def convert_single_pending_image():
    id = dir = file_name = None  # prevent NameError in except block
    try:
        result = database.get_single_pending_set_status_processing()
        if result is None:
            return False  # No pending image

        id, dir, file_name = result

        last_exception = None
        for attempt in range(config.OPENAI_CALLS_MAX_RETRIES):
            try:
                call_openai_api_and_save_image(dir, file_name)
                database.set_status_processed(id)
                return True
            except RetryableError as e:
                last_exception = e
                logger.warning(f"Retryable error (attempt {attempt + 1}/{config.OPENAI_CALLS_MAX_RETRIES}) during processing of image {file_name} (ID: {id}): {e}", exc_info=False)
                time.sleep(2 ** attempt) # exponential wait until next call
            except NonRetryableError as e:
                database.set_status_error(id, 'processing error', e)
                logger.error(f"Failed to process image {file_name} (ID: {id}): {e}", exc_info=False)
                break
            except Exception as e:
                database.set_status_error(id, 'processing error', e)
                logger.critical(f"Failed to process image {file_name} (ID: {id}): {e}", exc_info=False)
                break
        else: # If all retries fail (i.e., BREAK IS NEVER HIT), then else runs → raises the final failure
            logger.error(f"Failed to process image {file_name} (ID: {id}): {last_exception}", exc_info=False)  # all attempts failed
            database.set_status_error(id, 'processing error', last_exception)
            return True # continue with next img
            
    except Exception as e:
        if id is not None:
            database.set_status_error(id, 'processing error', e)
        if id and file_name:
            logger.error(f"Failed to process image {file_name} (ID: {id}): {e}", exc_info=False)
        else:
            logger.critical(f"Error during image processing: {e}", exc_info=True)

        return True  # continue processing others

def process_all_pending_images():
    while True:
        keep_going = convert_single_pending_image()
        if keep_going == False:
            logger.info("No more pending images")
            break  # EXIT LOOP IF NO MORE PENDINGS

if __name__ == "__main__":
    process_all_pending_images()
    # print(database.get_single_pending_set_status_processing())



# TODO
# kolumny errorType + errorMessage, appendować (z nową linią?)
# async dla requestów openai?
# nadpisywanie obrazkow jesli juz processed? (nie powinno sie zdazyc ale lepiej zrobic)
# timeouty poustawiać dla api
# rewrite db to get and update in one step (single db lock needed)
# error counters to stop the script?



# PYTANIA 1
# ile kompow/procesow ma generowac obrazki
# czy obrazki sciagamy w 1 duzym zipie czy pojedynczo
# gdzie uploadujemy i tez czy w bulku czy pojedynczo
# jakie formaty wejsciowe
# zapisujemy w tym samym miejscu, ale z inną nazwą? Usuwamy oryginał?