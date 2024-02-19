from flask import Blueprint, render_template, request, url_for, redirect
from database.database import fetch_all_threads_and_posts, add_post
from utils.data_parsers import parse_content, parse_request_images
from utils.data_rendering import render_all_posts, order_threads_by_recent
from wtforms import Form, StringField, SubmitField, validators

home = Blueprint('home', __name__)

class NewThreadForm(Form):
    title = StringField('title', validators=[validators.InputRequired(message="Title is empty!"), validators.Length(min=4, max=15, message="Title is too long or too short!")])
    content = StringField('content', validators=[validators.DataRequired(), validators.Length(min=4, max=15, message="Content is too long or too short!")])
    submit = SubmitField('post')

@home.route('/', methods=('GET', 'POST'))
def index():
    form = NewThreadForm(request.form)
    
    if request.method == 'POST' and form.validate():

        content = parse_content(form.content.data)
        title = form.title.data
        images = parse_request_images(request.files.getlist('image'))
        
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
        
    return render_template('index.html', threads=threads_data, posts=rendered_posts_data, form=form)
