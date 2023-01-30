from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
import urllib

from sweetbean import util
from sweetPeaEnglishTranslator import spet, sbet

translator = Blueprint("translator", __name__, template_folder="templates")


def convert(input):
    # Converts unicode to string
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, str):
        return input.encode("utf-8")
    else:
        return input


@translator.route("/sweetPea", methods=["GET", "POST"])
@login_required
def sweet():
    with open("sweetPeaEnglishTranslator/test/text_unformatted_2.txt") as f:
        text = f.read()
    code = ""
    form = FlaskForm()
    if request.method == "POST":
        if "formatText" in request.form:
            if "gpt3Text" in request.form:
                text = request.form["gpt3Text"]
                if spet.check_line_comments(text):
                    text = spet.uncomment_text(text)
                else:
                    text = spet.comment_text(text)
            if "gpt3Code" in request.form:
                code = request.form["gpt3Code"]
        elif "formatCode" in request.form:
            if "gpt3Code" in request.form:
                code = request.form["gpt3Code"]
                if spet.check_line_comments(code):
                    code = spet.uncomment_code(code)
                else:
                    code = spet.comment_code(code)
            if "gpt3Text" in request.form:
                text = request.form["gpt3Text"]
        elif "toCode" in request.form:
            if "gpt3Text" in request.form:
                text = text_ = request.form["gpt3Text"]
                if spet.check_line_comments(text):
                    text_ = spet.uncomment_text(text)
                text_ = urllib.parse.quote(convert(text_))
                return render_template(
                    "loading.html",
                    my_endpoint="/sweetPea",
                    my_function="text_to_code",
                    text=text_,
                    code=None,
                )
        elif "toText" in request.form:
            if "gpt3Code" in request.form:
                code = code_ = request.form["gpt3Code"]
                if spet.check_line_comments(code):
                    code_ = spet.uncomment_code(code)
                code_ = urllib.parse.quote(convert(code_))
                return render_template(
                    "loading.html",
                    my_endpoint="/sweetPea",
                    my_function="code_to_text",
                    text=None,
                    code=code_,
                )
        elif "runPython" in request.form:
            file = open(
                f"sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/py_tmp.py",
                "r",
            ).read()
            exec(file, globals())
            return send_file(
                f"sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/seq_tmp_0.csv"
            )
        elif "getPdf" in request.form:
            return send_file(
                f"sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/pdf_tmp.pdf"
            )
        elif "loading" in request.form:
            if request.form["my_function"] == "text_to_code":
                text = urllib.parse.unquote(request.form["text"])
                code = spet.text_to_code(
                    text,
                    f"spet/{current_user.id}/py_tmp.py",
                    f"sweetPeaEnglishTranslator/translator/output/spet/{current_user.id}/seq_tmp",
                )
                return render_template(
                    "sweetPea.html",
                    title="Sweet",
                    form=form,
                    text=text,
                    code=code,
                    user=current_user,
                )
            elif request.form["my_function"] == "code_to_text":
                code = urllib.parse.unquote(request.form["code"])
                text = spet.code_to_text(code, "pdf_tmp.pdf")
                text = spet.uncomment_text(text)
                return render_template(
                    "sweetPea.html",
                    title="Sweet",
                    form=form,
                    text=text,
                    code=code,
                    user=current_user,
                )

    return render_template(
        "sweetPea.html",
        title="Sweet",
        form=form,
        text=text,
        code=code,
        user=current_user,
    )


@translator.route("/sourPea", methods=["GET", "POST"])
@login_required
def sour():
    with open("sweetPeaEnglishTranslator/test/text_unformatted_1.txt") as f:
        original = f.read()
    translation = ""
    form = FlaskForm()
    if request.method == "POST":
        if "textToText" in request.form:
            if "gpt3Original" in request.form:
                original = request.form["gpt3Original"]
                original, translation = spet.text_to_text(original)
        elif "codeToCode" in request.form:
            if "gpt3Original" in request.form:
                original = request.form["gpt3Original"]
                original, translation = spet.code_to_code(original)
    return render_template(
        "sourPea.html",
        title="Sour",
        form=form,
        original=original,
        translation=translation,
        user=current_user,
    )


@translator.route("/jsPsych", methods=["GET", "POST"])
@login_required
def psych():
    with open("sweetPeaEnglishTranslator/test/to_experiment/text_np_full_1.txt") as f:
        text = f.read()
    code = ""
    form = FlaskForm()
    if request.method == "POST":
        if "formatText" in request.form:
            if "gpt3Text" in request.form:
                text = request.form["gpt3Text"]
                if sbet.check_line_comments(text):
                    text = sbet.uncomment_text(text)
                else:
                    text = sbet.comment_text(text)
            if "gpt3Code" in request.form:
                code = request.form["gpt3Code"]
        elif "formatCode" in request.form:
            if "gpt3Code" in request.form:
                code = request.form["gpt3Code"]
                if sbet.check_line_comments(code):
                    code = sbet.uncomment_code(code)
                else:
                    code = sbet.comment_code(code)
            if "gpt3Text" in request.form:
                text = request.form["gpt3Text"]
        elif "toCode" in request.form:
            if "gpt3Text" in request.form:
                text = text_ = request.form["gpt3Text"]
                if sbet.check_line_comments(text):
                    text_ = sbet.uncomment_text(text)
                text_ = urllib.parse.quote(convert(text_))
                return render_template(
                    "loading.html",
                    my_endpoint="/jsPsych",
                    my_function="text_to_code",
                    text=text_,
                    code=None,
                )
        elif "toText" in request.form:
            if "gpt3Code" in request.form:
                code = code_ = request.form["gpt3Code"]
                if sbet.check_line_comments(code):
                    code_ = sbet.uncomment_code(code)
                code_ = urllib.parse.quote(convert(code_))
                return render_template(
                    "loading.html",
                    my_endpoint="/jsPsych",
                    my_function="code_to_text",
                    text=None,
                    code=code_,
                )
        elif "runPython" in request.form:
            file = open(
                r"sweetPeaEnglishTranslator/translator/output/sbet/py_tmp.py", "r"
            ).read()
            exec(file, globals())
            util.create_html(
                "sweetPeaEnglishTranslator/translator/output/sbet/out.js",
                "flask/templates/experiment.html",
            )
            return render_template("experiment.html")
        elif "getPdf" in request.form:
            return send_file(
                "sweetPeaEnglishTranslator/translator/output/sbet/pdf_tmp.pdf"
            )
        elif "loading" in request.form:
            if request.form["my_function"] == "text_to_code":
                text = urllib.parse.unquote(request.form["text"])
                code = sbet.text_to_code(text, "sbet/py_tmp.py")
                return render_template(
                    "jsPsych.html",
                    title="Psych",
                    form=form,
                    text=text,
                    code=code,
                    user=current_user,
                )
            elif request.form["my_function"] == "code_to_text":
                code = urllib.parse.unquote(request.form["code"])
                text = sbet.code_to_text(code, "pdf_tmp.pdf")
                text = spet.uncomment_text(text)
                return render_template(
                    "jsPsych.html",
                    title="Psych",
                    form=form,
                    text=text,
                    code=code,
                    user=current_user,
                )

    return render_template(
        "jsPsych.html",
        title="Psych",
        form=form,
        text=text,
        code=code,
        user=current_user,
    )
