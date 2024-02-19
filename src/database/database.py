import sqlite3

from utils.disk_operators import write_image
from globals import *

def get_db_connection():
    conn = sqlite3.connect(CURSOR_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table(connection):
    schema_threads = """
    CREATE TABLE {} (
        {} INTEGER PRIMARY KEY AUTOINCREMENT,
        {} INTEGER,
        {} TEXT NOT NULL
    );
    """.format(THREADS_TABLE_NAME, THREADS_ID, THREADS_ORIGINAL_POST_ID, THREADS_TITLE)

    schema_posts = """
    CREATE TABLE {} (
        {} INTEGER PRIMARY KEY AUTOINCREMENT,
        {} INTEGER,
        {} INTEGER,
        {} TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        {} TEXT NOT NULL,
        {} TEXT,
        {} INTEGER,
        {} INTEGER
    );
    """.format(POSTS_TABLE_NAME, POSTS_ID, POSTS_ID_IN_THREAD,POSTS_THREAD_ID, POSTS_DATE_TIME, POSTS_CONTENT, POSTS_SENDER_IP,POSTS_IMAGES, POSTS_IS_DELETED)

    schema_images = """
    CREATE TABLE {} (
        {} INTEGER PRIMARY KEY AUTOINCREMENT,
        {} INTEGER,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL,
        {} TEXT NOT NULL
    );
    """.format(IMAGES_TABLE_NAME, IMAGES_ID, IMAGES_POST_ID,IMAGES_FILE_NAME, IMAGES_RESOLUTION, IMAGES_SIZE, IMAGES_EXTENSION)

    connection.executescript(schema_threads + schema_posts + schema_images)

def fetch_all_threads_and_posts():
    threads_data = []
    posts_data = []

    conn = get_db_connection()
    threads = conn.execute('SELECT * FROM {};'.format( THREADS_TABLE_NAME)).fetchall()
    for thread in threads:
        thread_data = dict(thread)
        threads_data.append(thread_data)

        posts = conn.execute("SELECT * FROM {} WHERE {}=?;".format(POSTS_TABLE_NAME, POSTS_THREAD_ID), (thread_data[THREADS_ID], )).fetchall()
        
        # at this point probably should select only N posts where N==3 ?
        posts_list = []
        for post in posts: 
            post = dict(post)
            db_images = conn.execute("SELECT * FROM {} WHERE {}=?;".format(IMAGES_TABLE_NAME, IMAGES_POST_ID), (post[POSTS_ID], )).fetchall()
            post['images'] = [dict(image) for image in db_images]
            posts_list.append(post)
        
        posts_data.append(posts_list)
   
    conn.close()
    return threads_data, posts_data

def get_post_by_id(variable):
    conn = get_db_connection()
    try:
        post = conn.execute("SELECT * FROM {} WHERE {}=?;".format(POSTS_TABLE_NAME, POSTS_ID), (variable, )).fetchall()[0]
        post = dict(post)
        images = conn.execute("SELECT * FROM {} WHERE {}=?;".format(IMAGES_TABLE_NAME, IMAGES_POST_ID), (post[POSTS_ID], )).fetchall()
        post['images'] = [dict(image) for image in images]
    except IndexError: # TODO: replace with a better way to check posts
        return None
    conn.close()
    return post

def get_posts_by_thread_id(thread_id):
    post_list = []
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM {} WHERE {}=?;".format(POSTS_TABLE_NAME, POSTS_THREAD_ID), (thread_id, )).fetchall()
    for post in posts:
        post = dict(post)
        images = conn.execute("SELECT * FROM {} WHERE {}=?;".format(IMAGES_TABLE_NAME, IMAGES_POST_ID), (post[POSTS_ID], )).fetchall()
        post['images'] = [dict(image) for image in images]
        post_list.append(post)
    conn.close()
    return post_list

def get_thread_data_by_thread_id(thread_id):
    conn = get_db_connection()
    thread_data = dict(conn.execute("SELECT * FROM {} WHERE {}=?;".format(THREADS_TABLE_NAME, THREADS_ID), (thread_id, )).fetchall()[0])
    conn.close()
    return thread_data

def get_last_thread_id(connection):
    try:
        return dict(connection.execute("SELECT {} FROM {} ORDER BY {} DESC LIMIT 1;".format(THREADS_ID, THREADS_TABLE_NAME, THREADS_ID)).fetchall()[0])[THREADS_ID]
    except IndexError:
        return 0

def get_last_post_id(connection):
    try:
        return dict(connection.execute("SELECT {} FROM {} ORDER BY {} DESC LIMIT 1;".format(POSTS_ID, POSTS_TABLE_NAME, POSTS_ID)).fetchall()[0])[POSTS_ID]
    except IndexError:
        return 0

def get_last_image_id(connection):
    try:
        return dict(connection.execute("SELECT {} FROM {} ORDER BY {} DESC LIMIT 1;".format(IMAGES_ID, IMAGES_TABLE_NAME, IMAGES_ID)).fetchall()[0])[IMAGES_ID]
    except IndexError:
        return 0

def get_last_post_in_thread_id(connection, thread_id):
    try:
        return dict(connection.execute("SELECT * FROM {} WHERE {}=? ORDER BY {} DESC LIMIT 1;".format(POSTS_TABLE_NAME, POSTS_THREAD_ID, POSTS_ID_IN_THREAD), (thread_id, )).fetchall()[0])[POSTS_ID_IN_THREAD]
    except IndexError:
        return 0

def insert_thread_to_db(connection, title, original_post_id):
    connection.execute("INSERT INTO {} VALUES (NULL, ?, ?)".format(THREADS_TABLE_NAME), (original_post_id, title))

def insert_post_to_db(connection, post_in_thread_id, thread_id, post_content, sender_ip, num_images, is_deleted=0):
    connection.execute('INSERT INTO {} VALUES (NULL, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?, ?)'.format(POSTS_TABLE_NAME),
        (post_in_thread_id, 
        thread_id,
        post_content,
        sender_ip,
        num_images,
        is_deleted))

def add_image_to_db(connection, image, post_id):
    connection.execute('INSERT INTO {} VALUES (NULL, ?, ?, ?, ?, ?)'.format(IMAGES_TABLE_NAME),
        (post_id, 
        image['filename'], 
        image['resolution'], 
        image['size'],
        image['extension']))

def add_post(new_thread, post_content, sender_ip, images, thread_id=None, title=None):
    connection = get_db_connection()

    if new_thread:
        # I need `thread_id` to insert the post in the database,
        #   so I'm trying to retrieve posts's ID in advance.
        #   If there are no posts in the DB, I just assign 0.
        # TODO: find a more optimal way to do so maybe?
        inserted_post_id = get_last_post_id(connection) + 1
        insert_thread_to_db(connection, title, inserted_post_id)
        thread_id = get_last_thread_id(connection)

    inserted_post_in_thread_id = get_last_post_in_thread_id(connection, thread_id) + 1
    num_images = 0
    if images is not None:
        num_images = len(images)
    insert_post_to_db(connection, inserted_post_in_thread_id, thread_id, post_content, sender_ip, num_images)

    post_id = get_last_post_id(connection)

    if images is not None:
        for image in images:
            add_image_to_db(connection, image, post_id)
            image_id = get_last_image_id(connection)
            write_image(image['file'], image_id, image['extension'])

    connection.commit()
    connection.close()