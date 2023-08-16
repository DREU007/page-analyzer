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
import pathlib 
import json


LOCALES_FP = 'page_analyzer/locales.json'

class Locales:
    def __init__(self, fp=LOCALES_FP):
        fp = pathlib.Path().absolute().joinpath(fp)
        self.locales = json.loads(fp.read_text())


    def get_kv_dict(self, lang):
        return self.locales[lang] | self.locales['languages']

