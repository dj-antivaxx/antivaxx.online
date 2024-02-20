import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlite3

from blueprints.home import home as home_blueprint
from blueprints.thread import thread_bp as thread_blueprint

from database.database import add_post, create_table

from globals import DATABASE_PATH, CURSOR_PATH, ARTIFACTS_DIR, UPLOADS_DIR


if __name__ == '__main__':
    app = Flask(__name__)
    app.debug = True

    app.register_blueprint(home_blueprint)
    app.register_blueprint(thread_blueprint)

    os.makedirs(UPLOADS_DIR, exist_ok=True)
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join('..', DATABASE_PATH))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['UPLOAD_FOLDER'] = UPLOADS_DIR

    connection = sqlite3.connect(CURSOR_PATH)

    # Populate DB with test thread
    try:
        connection.execute("SELECT * FROM threads;")
    except sqlite3.OperationalError:
        create_table(connection)
        add_post(
            new_thread=True,
            post_content="Hello World",
            sender_ip=None, 
            images=None,
            thread_id=None,
            title="Test thread!"
        )
    
    db = SQLAlchemy()
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    connection.close
   
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
