import os
from flask import (
        Flask, render_template, redirect, url_for, make_response, request, flash,
        get_flashed_messages
)
import psycopg2
import psycopg2.extras

from page_analyzer.locales_loader import Locales
from page_analyzer.url_tools import normalize, validate
from page_analyzer.db_processor import DB

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(
        DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor
)
db = DB(conn)
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

@app.route('/urls', methods=['GET'])
def get_urls():
    sql_data = db.get_urls_data()
    return render_template('urls.html', table_data=sql_data) 

@app.route('/urls', methods=['POST'])
def post_urls():
    url = request.form.get('url', False)
    if not url:
        flash('invalid', 'danger')
        flash('missing', 'danger') 
        return make_response(redirect(url_for('get_index'), code=302))

    normalized_url = normalize(url)
    if not validate(normalized_url):
        flash('invalid', 'danger') 
        return make_response(redirect(url_for('get_index'), code=302))

    existing_urls = db.get_existing_urls()
    if normalized_url in existing_urls:
        flash('exist', 'info')
    else:
        db.insert_url(normalized_url)
        flash('added', 'success')

    url_id = db.get_url_id_by_name(normalized_url)
    return make_response(redirect(
        url_for('get_url_id', url_id=url_id), code=302
    ))

@app.route('/urls/<int:url_id>')
def get_url_id(url_id):
    messages = get_flashed_messages(with_categories=True)
    url_data = db.get_url_data(url_id)
    url_checks = db.get_checks_data(url_id)
    return render_template(
            'url_id.html',
            url_data=url_data,
            url_checks=url_checks,
            messages=messages
    )

@app.route('/urls/<int:url_id>/checks', methods=['POST'])
def post_url_id_checks(url_id):
    db.insert_check(url_id) 
    return redirect(url_for('get_url_id', url_id=url_id), 302)
