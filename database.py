import sqlite3
import time
import logging
import config
from datetime import datetime
import sqlite3
import logger_setup

# Get local time as SQLite works in UTC
# datetime.now()

logger_setup.setup_logging()
logger = logging.getLogger(__name__)

ALLOWED_STATUSES = "('pending', 'processing', 'processed', 'error', 'done')"
TABLE_CREATION_QUERY = f"""
CREATE TABLE IF NOT EXISTS {config.DATABASE_TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir TEXT NOT NULL,
    file_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN {ALLOWED_STATUSES}),
    time_indexed DATETIME,
    time_proc_start DATETIME,
    time_proc_end DATETIME,
    time_sent DATETIME,
    error_types TEXT,
    error_messages TEXT,
    notes TEXT,
    UNIQUE(dir, file_name)
)"""

def database_connection(timeout_seconds=5.0):
    return sqlite3.connect(config.DATABASE_PATH, timeout=timeout_seconds)

def create_table_if_necessary():
    with database_connection() as db:
        db.execute(TABLE_CREATION_QUERY)
        # print("Database created/verified successfully.")

def insert_many(list_to_insert):
    start_time = time.time()
    current_datetime = datetime.now().replace(microsecond=0)
    with database_connection() as db:
        db.executemany(
            f"INSERT OR IGNORE INTO {config.DATABASE_TABLE_NAME} (dir, file_name, time_indexed) VALUES (?, ?, ?)",
            [
                (entry["dir"], entry["file_name"], current_datetime)
                for entry in list_to_insert
            ]
        )
        message = f"Inserted/Ignored {len(list_to_insert)} records in {round(time.time() - start_time, 1)}s"
    # print(message)
    logger.info(message)

def select_all():
    with database_connection() as db:
        cursor = db.execute(f"SELECT COUNT(*) FROM {config.DATABASE_TABLE_NAME}")
        count = cursor.fetchone()[0]
        message = f"{count} records found in DB"
    logger.info(message)
    # print(message)

def get_single_pending_set_status_processing():
    current_datetime = datetime.now().replace(microsecond=0)
    with database_connection() as db:
        # ORDER BY id to process files in db order
        # SINGLE TRANSACTION TO LOCK THE DB FROM ANOTHER READ ATTEMPTS
        row = db.execute(f"""
            UPDATE {config.DATABASE_TABLE_NAME}
            SET status = 'processing', time_proc_start = ?
            WHERE id = (
                SELECT id FROM {config.DATABASE_TABLE_NAME}
                WHERE status = 'pending'
                ORDER BY id
                LIMIT 1
            )
            RETURNING id, dir, file_name
        """, (current_datetime,)).fetchone()

        return row  # None if no pending

# def get_single_pending_set_status_processing():
#     current_datetime = datetime.now().replace(microsecond=0)
#     with database_connection() as db:
#         # ORDER BY id to process files in db order
#         row = db.execute(f"SELECT id, dir, file_name FROM {config.DATABASE_TABLE_NAME} WHERE status = 'pending' ORDER BY id LIMIT 1").fetchone()
#         if not row:
#             return None
#         id, dir, file_name = row

#         # Set status = 'processing' and time_proc_start
#         db.execute(f"UPDATE {config.DATABASE_TABLE_NAME} SET status = 'processing', time_proc_start = ? WHERE id = ?", (current_datetime, id))

#         return id, dir, file_name

def set_status_processed(id):
    current_datetime = datetime.now().replace(microsecond=0)
    with database_connection() as db:
        db.execute(f"UPDATE {config.DATABASE_TABLE_NAME} SET status = 'processed', time_proc_end = ? WHERE id = ?", (current_datetime, int(id)))

def set_status_done(id):
    current_datetime = datetime.now().replace(microsecond=0)
    with database_connection() as db:
        db.execute(f"UPDATE {config.DATABASE_TABLE_NAME} SET status = 'done', time_sent = ? WHERE id = ?", (current_datetime, int(id)))

# def set_status_error(id, error_type, error_message):
#     current_datetime = datetime.now().replace(microsecond=0)
#     with database_connection() as db:
#         db.execute(f"UPDATE {config.DATABASE_TABLE_NAME} SET status = 'error' WHERE id = ?", (int(id),))

        
def set_status_error(id, error_type, error_message):
    current_datetime = datetime.now().replace(microsecond=0)
    with database_connection() as db:
        # char(10)  = \n
        db.execute(f"""
            UPDATE {config.DATABASE_TABLE_NAME}
            SET status = 'error',
                error_types = COALESCE(error_types, '') || ? || char(10),
                error_messages = COALESCE(error_messages, '') || ? || char(10) || char(10)
            WHERE id = ?;
        """, (str(error_type), str(error_message), int(id)))