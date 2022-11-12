from flask import Flask, render_template, request, send_file
from sweetPeaEnglishTranslator.myConfig import MyConfig
from flask_wtf import FlaskForm
from sweetPeaEnglishTranslator.translator import translate
from sweetPeaEnglishTranslator import spet
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
        if 'formatText' in request.form:
            if 'gpt3Text' in request.form:
                text = request.form['gpt3Text']
                if spet.check_line_comments(text):
                    text = spet.uncomment_text(text)
                else:
                    text = spet.comment_text(text)
            if 'gpt3Code' in request.form:
                code = request.form['gpt3Code']
        elif 'toCode' in request.form:
            if 'gpt3Text' in request.form:
                text = text_ = request.form['gpt3Text']
                if spet.check_line_comments(text):
                    text_ = spet.uncomment_text(text)
                code = spet.text_to_code(text_, 'sweetPeaEnglishTranslator/temp/exp_tmp.py',
                                         'sweetPeaEnglishTranslator/temp/seq_tmp')
            elif 'gpt3Code' in request.form:
                code = request.form['gpt3Code']
        elif 'runPython' in request.form:
            file = open(r'sweetPeaEnglishTranslator/temp/exp_tmp.py', 'r').read()
            print(file)
            exec(file, globals())
            return send_file('sweetPeaEnglishTranslator/temp/seq_tmp_0.csv')
    return render_template('sweetPea.html', title='sweetPea', form=form, text=text, code=code)
