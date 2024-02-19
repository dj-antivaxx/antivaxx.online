from flask import Blueprint, render_template, request, url_for, flash, redirect
from database.database import fetch_all_threads_and_posts, add_post
from utils.data_parsers import parse_content, parse_request_images
from utils.data_rendering import render_all_posts, order_threads_by_recent

home = Blueprint('home', __name__)


@home.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':

        content = parse_content(request.form['content'])
        title = request.form['title']
        images = parse_request_images(request.files.getlist('image'))

        if content is None:
            flash('Content is required!')
            return redirect(url_for('home.index'))
        
        if title is None:
            flash('Title is required!')
            return redirect(url_for('home.index'))
        
        new_thread = True
        sender_ip = None
        thread_id = None
        add_post(new_thread, content, sender_ip, images, thread_id, title)
  
        return redirect(url_for('home.index'))
    
    threads_and_posts_data = fetch_all_threads_and_posts()
    threads_and_posts_data = order_threads_by_recent(threads_and_posts_data)

    posts_data = [data['posts_data'] for data in threads_and_posts_data]
    threads_data = [data['thread_data'] for data in threads_and_posts_data]
    rendered_posts_data = render_all_posts(posts_data)

    return render_template('index.html', threads=threads_data, posts=rendered_posts_data)
