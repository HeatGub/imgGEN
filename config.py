import logging

# FILES/DIRS PROPERTIES
ROOT_DIR = "D:/imgGEN/paths/create/samples" # will scan everything inside this dir and index files with allowed extension to database 
ALLOWED_INPUT_IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg"}
OUTPUT_IMAGE_EXTENSION = "webp"

# DATABASE
DATABASE_PATH = "database.db" # keep in the same directory as main.py
DATABASE_TABLE_NAME = "images"

# OPENAI
OPENAI_CALLS_MAX_RETRIES = 3
OPENAI_API_KEY = "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"
OPENAI_TIMEOUT_SECONDS = 20
OPENAI_PROMPT = """Create a professional studio product photo using the attached image as reference. 
The product should appear in a close-up shot, centered, and filling most of the frame. 
Use a plain white background, soft lighting, and subtle shadows to emphasize depth and texture. 
Preserve the original product's shape, material, colors and labels.
Preserving the exact label text, placement, and visual identity is crucial.
The goal is to use this for an advertisement — it must look clean, sharp, and text must be readable."""

# LOGGING - DEBUG / INFO / WARNING / ERROR / CRITICAL
LOGGING_LEVEL_FILE = logging.WARNING
LOGGING_LEVEL_CONSOLE = logging.INFO