import os
import datetime
import psycopg2
import psycopg2.extras
from flask import (
        Flask, render_template, redirect, url_for, make_response, request, flash,
        get_flashed_messages
)
from page_analyzer.locales_loader import Locales
from page_analyzer.url_tools import normalize, validate

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(
        DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor
)
curr = conn.cursor()
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
    curr.execute("SELECT * FROM urls ORDER BY id DESC;")
    sql_data = curr.fetchall()
    return render_template('urls.html', table_data=sql_data) 

def get_existing_urls():
    curr.execute('SELECT name FROM urls;')
    sql_data = curr.fetchall()
    if sql_data:
        return [row['name'] for row in sql_data]
    return []

def insert_url(normalized_url):
    curr.execute(
        'INSERT INTO urls (name, created_at) VALUES (%s, %s);',
        (normalized_url, datetime.datetime.now().isoformat())
    )
    conn.commit()

def get_url_id_by_name(normalized_url):
    curr.execute('SELECT id FROM urls WHERE name = %s', (normalized_url,))
    url_id = curr.fetchone()['id']
    return url_id

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

    existing_urls = get_existing_urls()
    if normalized_url in existing_urls:
        flash('exist', 'info')
    else:
        insert_url(normalized_url)
        flash('added', 'success')

    url_id = get_url_id_by_name(normalized_url)
    return make_response(redirect(
        url_for('get_url_id', url_id=url_id), code=302
    ))
    
@app.route('/urls/<int:url_id>')
def get_url_id(url_id):
    messages = get_flashed_messages(with_categories=True)
    curr.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
    url_data = curr.fetchone()
    return render_template('url_id.html', url_data=url_data, messages=messages)
