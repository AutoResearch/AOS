from flask import Flask, render_template, request
from sweetPeaEnglishTranslator.myConfig import MyConfig
from flask_wtf import FlaskForm
from sweetPeaEnglishTranslator.translator import translate
import os

_dir = os.path.dirname(__file__)
template_dir = os.path.join(_dir, 'flask/templates')
static_dir = os.path.join(_dir, 'flask/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(MyConfig)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', titel='Home')


@app.route('/sweetPea', methods=['GET', 'POST'])
def sweet():
    with open('sweetPeaEnglishTranslator/test/text_unformatted_1.txt') as f:
        text = f.read()
    code = ''
    form = FlaskForm()
    if request.method == 'POST':
        if request.form['toCode']:
            text = request.form['gpt3Text']
            code_tmp = translate.text_to_formatted(text)
            code = translate.text_to_code(code_tmp)
    return render_template('sweetPea.html', title='sweetPea', form=form, text=text, code=code)
