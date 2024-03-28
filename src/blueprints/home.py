from flask import Blueprint, render_template, request, url_for, redirect
from database.database import fetch_all_threads_and_posts, add_post
from utils.data_parsers import parse_content, parse_request_images
from utils.data_rendering import render_all_posts, order_threads_by_recent
from globals import IMAGE_MAX_RESOLUTION_X, IMAGE_MAX_RESOLUTION_Y
from wtforms import Form, SubmitField, TextAreaField, validators

home = Blueprint('home', __name__)

class NewThreadForm(Form):
    title = TextAreaField('Title', validators=[
        validators.InputRequired(message="Thread name please!"), 
        validators.Length(min=4, message="Title is too short!"), 
        validators.Length(max=15, message="Title is too long!")],
        render_kw={'rows': 1, 'cols': 50, 'style':'resize:none;','placeholder': 'Thread title! Min. 4 symbols :)'})
    content = TextAreaField('Text', validators=[
        validators.InputRequired(message="What about some content? :("), 
        validators.Length(min=4, message="Not enough content! :("), 
        validators.Length(max=1000, message="Too much content!")], 
        render_kw={'rows': 10, 'cols': 50, 'style':'resize:none;', 'placeholder': 'Thread content! Markdown supported and min. 4 symbols!'})
    submit = SubmitField('Submit!')

@home.route('/', methods=('GET', 'POST'))
def index():
    form = NewThreadForm(request.form)
    image_error = None
    
    if request.method == 'POST' and form.validate():
        images = parse_request_images(request.files.getlist('image'))
        # this is a weird gimmick but i did try file uploader in the wtforms 
        ## and it did not populate the files to form... idk
        ## TODO: maybe fix this when i have time??? 
        if not images:
            image_error = 'No images uploaded!'
        # TODO: move to a method
        elif any([image['resolution_x'] > IMAGE_MAX_RESOLUTION_X for image in images]) or any([image['resolution_y'] > IMAGE_MAX_RESOLUTION_Y for image in images]):
            image_error = 'Image too big!'
        elif any([image['extension'] not in ['.jpeg', '.gif', '.png', '.jpg'] for image in images]):
            image_error = 'Image file format not supported!'
        else:
            content = parse_content(form.content.data)
            title = form.title.data
            
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
        
    return render_template('index.html', threads=threads_data, posts=rendered_posts_data, form=form, image_error=image_error)
