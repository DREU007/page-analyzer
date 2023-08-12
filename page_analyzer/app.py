from flask import (
        Flask, render_template, redirect, url_for, make_response
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


@app.route('/')
def get_index():
    language = request.cookies.get('lang', 'eng')
    resposnse = make_response(
        render_template(
            'index.html',
            kv_dict=values[language],
            lang=values['languages']
        )
    )
    return resposnse

@app.route('/ru/')
def get_ru_index():
    return render_template(
        'index.html',
        kv_dict=values['rus'],
        lang=values['languages']
    )

@app.route('/en/')
def get_eng_index():
    return redirect(
        url_for('get_index'),
        code=302
    )

@app.errorhandler(404)
def not_found(e):
    return render_template(
        '404.html'
    )
