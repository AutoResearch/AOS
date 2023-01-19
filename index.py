from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from sweetPeaEnglishTranslator import spet, sbet
from sweetbean import util
import os
import urllib.parse

_dir = os.path.dirname(__file__)
template_dir = os.path.join(_dir, 'flask/templates')
static_dir = os.path.join(_dir, 'flask/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = 'something_secret'  # .from_object(MyConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
encrypter = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

KEY = 'Musslick_autoos_2023'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


DEBUG = True


# DB
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


with app.app_context():
    db.create_all()


class SignUpForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    key = PasswordField(render_kw={"placeholder": "Key"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user_names = User.query.filter_by(username=username.data).first()
        if existing_user_names:
            raise ValidationError(
                "The username already exists. Please choose a different username."
            )

    def validate_key(self, key):
        if key.data != KEY:
            raise ValidationError(
                "The provided key is not valid."
            )


class LogInForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Log In')


def convert(input):
    # Converts unicode to string
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if encrypter.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('sweet'))
            return render_template('login.html', form=form, title='Login', user=current_user, myError='password')
        return render_template('login.html', form=form, title='Login', user=current_user, myError='username')
    return render_template('login.html', form=form, title='Login', user=current_user, myError=False)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_pw = encrypter.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form, title='Signup', user=current_user)


@app.route('/index')
def index():
    return render_template('index.html', title='About', user=current_user)


@app.route('/sweetPea', methods=['GET', 'POST'])
@login_required
def sweet():
    with open('sweetPeaEnglishTranslator/test/text_unformatted_2.txt') as f:
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
                text_ = urllib.parse.quote(convert(text_))
                return render_template('loading.html', my_endpoint='/sweetPea', my_function='text_to_code', text=text_,
                                       code=None)
        elif 'toText' in request.form:
            if 'gpt3Code' in request.form:
                code = code_ = request.form['gpt3Code']
                if spet.check_line_comments(code):
                    code_ = spet.uncomment_code(code)
                code_ = urllib.parse.quote(convert(code_))
                return render_template('loading.html', my_endpoint='/sweetPea', my_function='code_to_text', text=None,
                                       code=code_)
        elif 'runPython' in request.form:
            file = open(f'sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/py_tmp.py', 'r').read()
            exec(file, globals())
            return send_file(f'sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/seq_tmp_0.csv')
        elif 'getPdf' in request.form:
            return send_file(f'sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/pdf_tmp.pdf')
        elif 'loading' in request.form:
            if request.form['my_function'] == 'text_to_code':
                text = urllib.parse.unquote(request.form['text'])
                code = spet.text_to_code(text, f'spet/{current_user.id}/py_tmp.py',
                                         f'sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/seq_tmp')
                return render_template('sweetPea.html', title='Sweet', form=form, text=text, code=code,
                                       user=current_user)
            elif request.form['my_function'] == 'code_to_text':
                code = urllib.parse.unquote(request.form['code'])
                text = spet.code_to_text(code, 'pdf_tmp.pdf')
                text = spet.uncomment_text(text)
                return render_template('sweetPea.html', title='Sweet', form=form, text=text, code=code,
                                       user=current_user)

    return render_template('sweetPea.html', title='Sweet', form=form, text=text, code=code, user=current_user)


@app.route('/sourPea', methods=['GET', 'POST'])
@login_required
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
    return render_template('sourPea.html', title='Sour', form=form, original=original, translation=translation,
                           user=current_user)


@app.route('/jsPsych', methods=['GET', 'POST'])
@login_required
def psych():
    with open('sweetPeaEnglishTranslator/test/to_experiment/text_np_full_1.txt') as f:
        text = f.read()
    code = ''
    form = FlaskForm()
    if request.method == 'POST':
        if 'formatText' in request.form:
            if 'gpt3Text' in request.form:
                text = request.form['gpt3Text']
                if sbet.check_line_comments(text):
                    text = sbet.uncomment_text(text)
                else:
                    text = sbet.comment_text(text)
            if 'gpt3Code' in request.form:
                code = request.form['gpt3Code']
        elif 'formatCode' in request.form:
            if 'gpt3Code' in request.form:
                code = request.form['gpt3Code']
                if sbet.check_line_comments(code):
                    code = sbet.uncomment_code(code)
                else:
                    code = sbet.comment_code(code)
            if 'gpt3Text' in request.form:
                text = request.form['gpt3Text']
        elif 'toCode' in request.form:
            if 'gpt3Text' in request.form:
                text = text_ = request.form['gpt3Text']
                if sbet.check_line_comments(text):
                    text_ = sbet.uncomment_text(text)
                text_ = urllib.parse.quote(convert(text_))
                return render_template('loading.html', my_endpoint='/jsPsych', my_function='text_to_code', text=text_,
                                       code=None)
        elif 'toText' in request.form:
            if 'gpt3Code' in request.form:
                code = code_ = request.form['gpt3Code']
                if sbet.check_line_comments(code):
                    code_ = sbet.uncomment_code(code)
                code_ = urllib.parse.quote(convert(code_))
                return render_template('loading.html', my_endpoint='/jsPsych', my_function='code_to_text', text=None,
                                       code=code_)
        elif 'runPython' in request.form:
            file = open(r'sweetPeaEnglishTranslator/translator/output/sbet/py_tmp.py', 'r').read()
            exec(file, globals())
            util.create_html('sweetPeaEnglishTranslator/translator/output/sbet/out.js',
                             'flask/templates/experiment.html')
            return render_template('experiment.html')
        elif 'getPdf' in request.form:
            return send_file('sweetPeaEnglishTranslator/translator/output/sbet/pdf_tmp.pdf')
        elif 'loading' in request.form:
            if request.form['my_function'] == 'text_to_code':
                text = urllib.parse.unquote(request.form['text'])
                code = sbet.text_to_code(text, 'sbet/py_tmp.py')
                return render_template('jsPsych.html', title='Psych', form=form, text=text, code=code,
                                       user=current_user)
            elif request.form['my_function'] == 'code_to_text':
                code = urllib.parse.unquote(request.form['code'])
                text = sbet.code_to_text(code, 'pdf_tmp.pdf')
                text = spet.uncomment_text(text)
                return render_template('jsPsych.html', title='Psych', form=form, text=text, code=code,
                                       user=current_user)

    return render_template('jsPsych.html', title='Psych', form=form, text=text, code=code, user=current_user)


@app.route('/resources')
def resources():
    return render_template('resources.html', title='Resources', user=current_user)


@app.route('/team')
def team():
    return render_template('team.html', title='Team', user=current_user)


if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)
