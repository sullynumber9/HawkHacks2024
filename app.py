# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, render_template, \
    request  # from flask.ext.sqlalchemy import SQLAlchemy import logging
from logging import Formatter, FileHandler

from forms import *
import os
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import json
import webbrowser

import datetime

import quickstart
# hello world
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

with open("config.json") as f:
    config_data = json.load(f)

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "supersekrit"

# set config data
client_id = config_data["client_id"]
client_secret = config_data["client_secret"]
scope=["profile", "email"]
blueprint = make_google_blueprint(client_id, client_secret)
app.register_blueprint(blueprint, url_prefix="/login")

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def home():
    # TODO: if login or not
    data = {"output": "You are signed in!", "login": False}
    if not google.authorized:
        return render_template('pages/placeholder.home.html', data=data)
        
    if google.authorized:
        data["login"] = True

        quickstart.main()

        return render_template('pages/placeholder.home.html', data=data)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/login/google/authorized")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

    quickstart()


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
