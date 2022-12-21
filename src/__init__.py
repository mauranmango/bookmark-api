# do strukturojme aplikacionin pranda krijojme folderin src
# folderi src do mbaje gjithe source code
# -> config do mbaje database configurations, te gjitha modelet me te cilat do punojme
# -> constants do mbaje disa variabla qe nuk duam ti ndryshojme
# -> static do mbaje file si css, images, js etj
# -> templates do mbaje filet html
# -> services do mbaje konfigurimet per sherbimet si psh: email service etj
# -> tests do mbaje testet si psh unittest
# blueprints are meant to group related functionality together


import os

from flask import Flask

from src.auth import auth
from src.bookmark import bookmark
from src.database import db


# ky factory function do krijoje aplikacionin dhe do percaktoje disa konfigurime si dhe do migroje tabelat ne database
def create_app(test_config=None):

    # ky parameter i thote Flask-ut se kemi disa konfigurime
    app = Flask(__name__, instance_relative_config=True)

    # pra nqs nuk do kemi konfigurime atehere i percaktojme konfigurimet
    if test_config is None:

        # update-ojme konfigurimet me kete funksion
        app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_KEY'),
                                SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
                                SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
                                FLASK_APP=os.environ.get('FLASK_APP'))

    else:
        # nqs i ka konfigurimet atehere merri nga parametri test_config
        app.config.from_mapping(test_config)

    # pasi krijuam blueprints i rregjistrojme
    app.register_blueprint(auth)
    app.register_blueprint(bookmark)

    # do rregjistrojme db
    db.app = app
    db.init_app(app)

    # qe te funksionojne "gjerat" i percaktojme keto funksione create_app() dhe e bejme folderin src entry point
    @app.route('/index')
    @app.route('/')
    def index():
        return "Hello World"

    @app.route('/hello')
    def say_hello():
        return {'hello': 'world'}

    db.create_all()

    return app


if __name__ == "__main__":
    create_app()

# Hapat
# 1. Project introduction and demo
# 2. Project setup
# 3. Flask API folder structure
# 4. Flask API Blueprints
# 5. Database and Models setup
# 6. HTTPS Status Codes
# 7. User Registration
