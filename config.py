import logging

# FILES/DIRS PROPERTIES
ROOT_DIR = "D:/imgGEN/paths/create" # will scan everything inside this dir and index files with allowed extension to database 
ALLOWED_INPUT_IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg"}
OUTPUT_IMAGE_EXTENSION = "webp"

# DATABASE
DATABASE_PATH = "database.db" # keep in the same directory as main.py
DATABASE_TABLE_NAME = "images"

# OPENAI
OPENAI_API_KEY = "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"
OPENAI_CALLS_MAX_RETRIES = 2 # 0 is minimum. EXPONENTIAL WAIT: time.sleep(2 ** attempt) - so the longest one = 2^OPENAI_CALLS_MAX_RETRIES seconds
OPENAI_TIMEOUT_SECONDS = 70 # image generates for about 30 seconds, not less than that!

# OPENAI_PROMPT = """Create a professional studio product photo using the attached image as reference.
# The WHOLE PRODUCT MUST BE FULLY VISIBLE in the frame, centered, and proportionally scaled so NO PARTS ARE CUT OFF.
# Use a plain white background, soft even lighting, and subtle shadows to emphasize depth and texture.
# Preserve the original product’s exact shape, material, colors, label text, placement, and overall visual identity.
# The final image should be clean, sharp, and advertisement-ready, with all label text easily readable and undistorted."""

# OPENAI_PROMPT = """
# Create a professional studio product photo using the attached image as reference.
# - THE WHOLE PRODUCT MUST BE FULLY VISIBLE IN THE FRAME WITH NO PARTS CUT OFF UNDER ANY CIRCUMSTANCES
# - The product should be centered and proportionally scaled to fit entirely within the image boundaries
# - Maintain the original aspect ratio of the product; do NOT stretch or distort
# - Use a plain white background with soft, even lighting and subtle shadows to emphasize depth and texture
# - Preserve the original product’s exact shape, material, colors, and all label text, including placement and visual identity
# - The label text must be clearly readable, sharp, and undistorted
# - The final image should be clean, crisp, and suitable for professional advertising purposes"""

OPENAI_PROMPT = """Create a professional studio product photo using the attached image as reference.
- THE WHOLE PRODUCT MUST BE FULLY VISIBLE IN THE FRAME WITH NO PARTS CUT OFF UNDER ANY CIRCUMSTANCES.
- The product should be centered and proportionally scaled to fit entirely within the image boundaries.
- Maintain the original aspect ratio of the product; do NOT stretch, distort, or crop any part.
- It is acceptable to have some empty white space (padding) around the product so the entire product fits well inside the 1024x1024 frame without being cut off.
- Use a plain white background with soft, even lighting and subtle shadows to emphasize depth and texture.
- Preserve the original product’s exact shape, material, colors, and all label text, including placement and visual identity.
- The label text must be clearly readable, sharp, and undistorted.
- The final image should be clean, crisp, and suitable for professional advertising purposes."""

# EXIT ON ERRORS
ERROR_COUNTER_LIMIT = 5

# LOGGING - DEBUG / INFO / WARNING / ERROR / CRITICAL
LOGGING_LEVEL_FILE = logging.INFO
LOGGING_LEVEL_CONSOLE = logging.INFO