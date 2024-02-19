import markdown

from database.database import get_post_by_id

def render_all_posts(posts_data):
    return [render_thread_posts(thread_posts) for thread_posts in posts_data]

def render_thread_posts(thread_posts):
    return [render_post(post) for post in thread_posts]

def render_post(post):
    rendered_post = post
    rendered_lines = []
    for line in rendered_post['post_content'].split('<br>'):
        rendered_line = {}
        if line.startswith('>>'):
            rendered_line['text'] = line
            rendered_line['type'] = 'quote'
            quoted_post_id =  line.split('>>')[1]
            quoted_post = get_post_by_id(quoted_post_id)
            rendered_line['quoted_post'] = None
            if quoted_post is not None:
                rendered_line['quoted_post'] = render_post(quoted_post)
        else:
            rendered_line['text'] = markdown.markdown(line)
            rendered_line['type'] = 'text'
        rendered_lines.append(rendered_line)
    rendered_post['rendered_content'] = rendered_lines
    if post['images']:
        rendered_images = []
        for image in post['images']:
            rendered_image = image
            rendered_image['download_link'] = str(image['id']) + image['extension']
            rendered_images.append(rendered_image)
        rendered_post['images'] = rendered_images
    return rendered_post
    