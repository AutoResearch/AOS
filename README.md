# AOS
Automated Open Science

## How to use flask local server:
setup an account on https://openai.com/. Get beta access (or ask Sebastian or Younes for a key). 
In the sweetPeaEnglishTranslator folder add .env file with the OPENAI_KEY="..." (this is the key you get from https://openai.com/)
Then run the following commands in your command line:
<br>
windows
```
set FLASK_APP=index.py
```
mac
```
export FLASK_APP=index.py
```
finally
```
flask run
```

## Usage of the flask app:

### sweetPea text -> code
You can translate text to code and download a sequence.<br>
To get sweetPea code click on `to code`.<br>
You can also try creating text from code, comment and uncommend code... <br>
As soon as there is sweetPea code (can take a while) you can execute the code and download a sequence via `Get Sequence`

### sweetBean text -> experiment
You can translate a written stimulus timeline into code and try the created experiment.<br>
<b>WARNING: THIS IS EXPERIMENTAL AND WORKS ONLY FOR VERY FEW EXPERIMENTS</b>
This only works in conjunction with a fitting sweetPea trial sequence on the "SWEET" page.<br>
You can try this: Generate a trial sequence for a stroop experiment on the "SWEET" page and create it.(Get Sequence).
Then try describing a stimulus timeline (e.g. fixation, iti, target, feedback) on the "PSYCH" page.<br>
You can then try running the experiment.


