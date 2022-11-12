# AOS
Automated Open Science

## How to use flask local server:
setup an account on https://openai.com/. Get beta access (or ask Sebastian or Younes for a key). 
In the sweetPeaEnglishTranslator add .env file with the OPENAI_KEY="..." (this is the key you geht from https://openai.com/)
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
you can translate text to code and download a sequence.<br>
To get sweetPea code click on `to code`.<br>
As soon as there is sweetPea code (can take a while) you can execute the code and download a sequence via `Get Sequence`
