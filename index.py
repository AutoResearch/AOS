from flask import Flask, render_template, request, send_file
from sweetPeaEnglishTranslator.myConfig import MyConfig
from flask_wtf import FlaskForm
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
    return render_template('index.html', title='About')


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
        elif 'formatCode' in request.form:
            if 'gpt3Code' in request.form:
                code = request.form['gpt3Code']
                if spet.check_line_comments(code):
                    code = spet.uncomment_code(code)
                else:
                    code = spet.comment_code(code)
            if 'gpt3Text' in request.form:
                text = request.form['gpt3Text']
        elif 'toCode' in request.form:
            if 'gpt3Text' in request.form:
                text = text_ = request.form['gpt3Text']
                if spet.check_line_comments(text):
                    text_ = spet.uncomment_text(text)
                code = spet.text_to_code(text_, 'py_tmp.py', 'sweetPeaEnglishTranslator/translator/output/seq_tmp')
        elif 'toText' in request.form:
            if 'gpt3Code' in request.form:
                code = code_ = request.form['gpt3Code']
                if spet.check_line_comments(code):
                    code_ = spet.uncomment_code(code)
                text = spet.code_to_text(code_, 'pdf_tmp.pdf')
                text = spet.uncomment_text(text)
        elif 'runPython' in request.form:
            file = open(r'sweetPeaEnglishTranslator/translator/output/py_tmp.py', 'r').read()
            exec(file, globals())
            return send_file('sweetPeaEnglishTranslator/translator/output/seq_tmp_0.csv')
        elif 'getPdf' in request.form:
            return send_file('sweetPeaEnglishTranslator/translator/output/pdf_tmp.pdf')
    return render_template('sweetPea.html', title='Sweet', form=form, text=text, code=code)


@app.route('/sourPea', methods=['GET', 'POST'])
def sour():
    with open('sweetPeaEnglishTranslator/test/text_unformatted_1.txt') as f:
        original = f.read()
    translation = ''
    form = FlaskForm()
    if request.method == 'POST':
        if 'textToText' in request.form:
            if 'gpt3Original' in request.form:
                original = request.form['gpt3Original']
                original, translation = spet.text_to_text(original)
        elif 'codeToCode' in request.form:
            if 'gpt3Original' in request.form:
                original = request.form['gpt3Original']
                original, translation = spet.code_to_code(original)
    return render_template('sourPea.html', title='Sour', form=form, original=original, translation=translation)


@app.route('/jsPsych', methods=['GET', 'POST'])
def psych():
    return render_template('jsPsych.html', title='Psych')


@app.route('/resources')
def resources():
    return render_template('resources.html', title='Resources')


@app.route('/team')
def team():
    return render_template('team.html', title='Team')
