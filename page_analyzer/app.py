import os
from flask import (
        Flask, render_template, redirect, url_for, make_response, request, flash,
        get_flashed_messages
)
from page_analyzer.locales_loader import Locales
from page_analyzer.url_tools import normalize, validate

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
locales = Locales()


@app.context_processor
def inject_kv_dict():
    cookies_lang = request.cookies.get('language', 'eng')
    return dict(kv_dict=locales.get_kv_dict(cookies_lang))

@app.route('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)

@app.route('/ru/')
def get_ru_index():
    response = make_response(redirect(
        url_for('get_index'), code=302
    ))
    response.set_cookie('language', 'rus')
    return response

@app.route('/en/')
def get_eng_index():
    response = make_response(redirect(
        url_for('get_index'), code=302
    ))
    response.set_cookie('language', 'eng')
    return response
    
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.route('/urls', methods=['GET', 'POST'])
def urls():
    if request.method == 'POST':
        url = request.form.get('url', False)
        if url:
            if validate(normalize(url)):
                # if url in db:
                url_id = 1  # TODO: Update get_sql_id()
                flash('added', 'success')
                return make_response(redirect(
                    url_for('get_url_id', url_id=url_id), code=302))
            flash('invalid', 'danger')
        flash('missing', 'danger') 
    response = make_response(redirect(url_for('get_index'), code=302))
    return response

@app.route('/urls/<int:url_id>')
def get_url_id(url_id):
    messages = get_flashed_messages(with_categories=True)
    return render_template('url_id.html', url_data=url_id, messages=messages)
