import markdown

from datetime import datetime
import re

from database.database import get_post_by_id
from globals import POSTS_DATE_TIME, POSTS_IMAGES, POSTS_CONTENT, IMAGES_EXTENSION

def reformat_thread_id(thread_id):
    return int(thread_id) + 1

def order_threads_by_recent(threads_and_posts_data):
    # TODO: this mf prob could be optimized better. =/

    posts_data = [data['posts_data'] for data in threads_and_posts_data]
    thread_ids_and_most_recent_datetimes = [{'thread_id': thread_i, 'most_recent_datime': max([post[POSTS_DATE_TIME] for post in thread_posts])} for thread_i, thread_posts in enumerate(posts_data)]
    
    thread_bump_order = [reformat_thread_id(thread['thread_id']) for thread in list(sorted(thread_ids_and_most_recent_datetimes, key=lambda x: x['most_recent_datime'], reverse=True))]
    
    threads_and_posts_data.sort(key=lambda x: thread_bump_order.index(int(x['thread_id'])))
    return threads_and_posts_data

def render_all_posts(posts_data):
    return [render_thread_posts(thread_posts) for thread_posts in posts_data]

def render_thread_posts(thread_posts):
    return [render_post(post) for post in thread_posts]

def render_post(post):
    rendered_post = post
    rendered_lines = []
    # TODO: fix the finicky reply rendering pls [1]
    for line in rendered_post[POSTS_CONTENT].split('<br>'):
        rendered_line = {}
        if re.match(">>\d+$", line):
            print('reply find + {}'.format(line))
            rendered_line['text'] = line
            rendered_line['type'] = 'quote'
            quoted_post_id = line.split('>>')[1]
            quoted_post = get_post_by_id(quoted_post_id)
            rendered_line['quoted_post'] = None
            if quoted_post is not None:
                rendered_line['quoted_post'] = render_post(quoted_post)
        else:
            # TODO: fix the finicky reply rendering pls [2]
            rendered_line['text'] = markdown.markdown(re.sub(r">>\d+", "", line))
            print(rendered_line['text'])
            rendered_line['type'] = 'text'
        rendered_lines.append(rendered_line)
    rendered_post['rendered_content'] = rendered_lines
    if post[POSTS_IMAGES]:
        rendered_images = []
        for image in post[POSTS_IMAGES]:
            rendered_image = image
            rendered_image['download_link'] = str(image['id']) + image[IMAGES_EXTENSION]
            rendered_images.append(rendered_image)
        rendered_post[POSTS_IMAGES] = rendered_images
    if post[POSTS_DATE_TIME]:
        rendered_post[POSTS_DATE_TIME] = datetime.fromisoformat(post[POSTS_DATE_TIME]).strftime("%H:%M %B %d, %Y")
    return rendered_post
    