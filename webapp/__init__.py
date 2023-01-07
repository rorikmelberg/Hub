import os
import functools
from webapp.db import get_db
import webapp.SMSession as SMSession

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask, render_template, session
from flask import jsonify
from flask_session.__init__ import Session
from datetime import datetime

dateFormatString = '%Y-%m-%d %H:%M:%S.%f'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # app.config.from_object(__name__)
    Session(app)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    from . import smomo
    app.register_blueprint(smomo.bp)

    from . import brew
    app.register_blueprint(brew.bp)

    from . import sensors
    app.register_blueprint(sensors.bp)


    from . import db
    db.init_app(app)
    
    return app
