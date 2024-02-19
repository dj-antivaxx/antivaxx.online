from flask import Blueprint, render_template, request, url_for, flash, redirect
from database.database import fetch_all_threads_and_posts, add_post
from utils.data_parsers import parse_content, parse_request_images
from utils.data_rendering import render_all_posts

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
    
    threads_data, posts_data = fetch_all_threads_and_posts()
    rendered_posts_data = render_all_posts(posts_data)

    return render_template('index.html', threads=threads_data, posts=rendered_posts_data)
