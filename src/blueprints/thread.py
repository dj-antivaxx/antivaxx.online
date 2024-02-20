from flask import Blueprint, render_template, request, send_from_directory, url_for, redirect
from database.database import get_posts_by_thread_id, get_thread_data_by_thread_id, add_post
from utils.data_parsers import parse_content, parse_request_images
from utils.data_rendering import render_thread_posts
from wtforms import Form, TextAreaField, SubmitField, validators

from globals import RELATIVE_UPLOADS_DIR

thread_bp = Blueprint('thread', __name__)

class NewPost(Form):
    content = TextAreaField('Text', validators=[
        validators.InputRequired(message="Thread name please!"), 
        validators.Length(min=4, message="Not enough content! :("), 
        validators.Length(max=1000, message="Too much content!")], 
        render_kw={'rows': 10, 'cols': 50, 'placeholder': 'Thread content! Markdown supported and min. 4 symbols!'})
    submit = SubmitField('Submit!')

@thread_bp.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(RELATIVE_UPLOADS_DIR, filename)

@thread_bp.route('/thread/<thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    form = NewPost(request.form)

    if request.method == 'POST' and form.validate():

        content = parse_content(form.content.data)
        images = parse_request_images(request.files.getlist('image'))

        new_thread = False
        sender_ip = None
        title = None
        add_post(new_thread, content, sender_ip, images, thread_id, title)
        return redirect(url_for('thread.thread', thread_id=thread_id))
    
    thread_data = get_thread_data_by_thread_id(thread_id)
    thread_posts = get_posts_by_thread_id(thread_id)
    rendered_thread_posts = render_thread_posts(thread_posts)
        
    
    return render_template("thread.html", posts=rendered_thread_posts, thread=thread_data, form=form)

