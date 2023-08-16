from flask import (
        Flask, render_template, redirect, url_for, make_response, request
)
from page_analyzer.locales_loader import Locales


app = Flask(__name__)

locales = Locales()


@app.context_processor
def inject_kv_dict():
    cookies_lang = request.cookies.get('language', 'eng')
    return dict(kv_dict=locales.get_kv_dict(cookies_lang))

@app.route('/')
def get_index():
    return render_template('index.html')

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
    return render_template(
        '404.html'
    )

@app.route('/urls', methods=['GET', 'POST'])
def urls():
    return render_template('urls.html')

@app.route('/urls/<int:url_id>')
def get_url_id(url_id):
    return render_template('url_id.html', url_data=url_id)
