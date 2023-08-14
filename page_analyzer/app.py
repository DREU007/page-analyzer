from flask import (
        Flask, render_template, redirect, url_for, make_response, request
)


app = Flask(__name__)

values={
    'eng': {
        'title': 'Web Page Analyzer',
        'urls': 'URLs',
        'lang': 'Languages',
        'description': ' Validate web page SEO-adaptiveness',
        'button': 'VALIDATE'
    },
    'rus': {
        'title': 'Анализатор страниц',
        'urls': 'Сайты',
        'lang': 'Язык',
        'description': 'Бесплатно проверяйте сайты на SEO-пригодность',
        'button': 'ПРОВЕРИТЬ'
        },
    'languages': {
        'rus': 'Русский',
        'eng': 'English'
    }
}


def get_kv_dict(lang):
    return values[lang] | values['languages']

@app.context_processor
def inject_kv_dict():
    cookies_lang = request.cookies.get('language', 'eng')
    return dict(kv_dict=get_kv_dict(cookies_lang))

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
