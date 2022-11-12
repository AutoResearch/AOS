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