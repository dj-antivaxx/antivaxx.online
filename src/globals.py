import os

ARTIFACTS_DIR = 'artifacts'
UPLOADS_DIR = 'uploads'

DATABASE_PATH = os.path.join('./', ARTIFACTS_DIR, 'db.sqlite')
CURSOR_PATH = os.path.join('./', ARTIFACTS_DIR, 'database.db')

UPLOADS_PATH = os.path.join('./', UPLOADS_DIR)
RELATIVE_UPLOADS_DIR = os.path.join('..', UPLOADS_PATH)

THREADS_TABLE_NAME = "threads"
THREADS_ID = "id"
THREADS_ORIGINAL_POST_ID = "original_post_id"
THREADS_TITLE = "title"

POSTS_TABLE_NAME = "posts"
POSTS_ID = "id"
POSTS_ID_IN_THREAD = "id_in_thread"
POSTS_THREAD_ID = "thread_id"
POSTS_DATE_TIME = "date_time"
POSTS_CONTENT = "post_content"
POSTS_SENDER_IP = "sender_ip"
POSTS_IMAGES = "images"
POSTS_IS_DELETED = "is_deleted"

IMAGES_TABLE_NAME = "images"
IMAGES_ID = "id"
IMAGES_POST_ID = "post_id"
IMAGES_FILE_NAME = "file_name"
IMAGES_RESOLUTION = "resolution"
IMAGES_SIZE = "size"
IMAGES_EXTENSION = "extension"

def create_board(board_name):
    os.mkdir(os.path.join(ARTIFACTS_DIR, board_name))
