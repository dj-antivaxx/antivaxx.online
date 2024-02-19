from flask import Blueprint, render_template, request, url_for, flash, redirect, send_from_directory
from database.database import get_posts_by_thread_id, get_thread_data_by_thread_id, add_post
from utils.data_parsers import parse_content, parse_request_images
from utils.data_rendering import render_thread_posts

from globals import RELATIVE_UPLOADS_DIR

thread_bp = Blueprint('thread', __name__)

@thread_bp.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(RELATIVE_UPLOADS_DIR, filename)

@thread_bp.route('/thread/<thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    if request.method == 'POST':
        content = parse_content(request.form['content'])
        images = parse_request_images(request.files.getlist('image'))

        if content is None:
            flash('Content is required!')
            return redirect(url_for('thread.thread', thread_id=thread_id))

        new_thread = False
        sender_ip = None
        title = None
        add_post(new_thread, content, sender_ip, images, thread_id, title)

        return redirect(url_for('thread.thread', thread_id=thread_id))
    
    thread_data = get_thread_data_by_thread_id(thread_id)
    thread_posts = get_posts_by_thread_id(thread_id)
    rendered_thread_posts = render_thread_posts(thread_posts)
    
    return render_template("thread.html", posts=rendered_thread_posts, thread=thread_data)

