#!/usr/bin/env python3
'''3. Parametrize templates
'''
from flask import (
    Flask,
    render_template,
    request
)
from flask_babel import Babel


class Config:
    '''Config var to a Flask Babel'''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@app.route('/')
def main() -> str:
    '''Rendering html template'''
    return render_template('4-index.html')


@babel.localeselector
def get_locale() -> str:
    '''Determine the best match with our supported languages'''
    if 'locale' in request.args:
        # Check if the selected lang is supported in our app
        if request.args['locale'] in app.config['LANGUAGES']:
            return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
