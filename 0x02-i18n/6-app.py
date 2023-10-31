#!/usr/bin/env python3
'''3. Parametrize templates
'''
from flask import (
    Flask,
    render_template,
    request,
    g
)
from flask_babel import Babel
from typing import Dict, Union


class Config:
    '''Config var to a Flask Babel'''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route('/')
def main() -> str:
    '''Rendering html template'''
    return render_template('6-index.html')


@babel.localeselector
def get_locale() -> str:
    '''Determine the best match with our supported languages'''
    if 'locale' in request.args:
        # Check if the selected lang is supported in our app
        if request.args['locale'] in app.config['LANGUAGES']:
            return request.args['locale']
    elif g.user and g.user.get('locale') \
            and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[Dict, None]:
    '''returns a logined user'''
    if 'login_as' in request.args:
        user_id = int(request.args['login_as'])
        return users.get(user_id)
    return None


@app.before_request
def before_request() -> None:
    '''inject/deal before request'''
    g.user = get_user()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
