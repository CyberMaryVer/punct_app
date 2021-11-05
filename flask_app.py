import os
import time
import json
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask_cors import CORS

from punct import apply_punkt_to_text
from postprocess_txt import get_time_steps

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1024000
app.secret_key = "secret key"


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form['text']
    res = apply_punkt_to_text(raw_text=user_input)
    save_log(f'RESULT: {res}')

    return f'RESULT: {res}'


@app.route('/punct/', methods=['GET', 'POST'])
def txt2txt():
    try:
        user_input = request.form['text'] # if request.content_type == "application/x-www-form-urlencoded" \
            # else json.loads(request.json)['text']
        res = apply_punkt_to_text(raw_text=user_input)
        return {"res": res}
    except Exception as e:
        return {"error": f"{type(e)}: {e}"}


@app.route('/subtitles/', methods=['GET', 'POST'])
def subtitles():
    try:
        user_input = request.form['time_steps'] if request.content_type == "application/x-www-form-urlencoded" \
            else json.loads(request.json)['time_steps']
        user_input = json.loads(user_input)
        raw_text = ' '.join([item['word'] for item in user_input])
        res = apply_punkt_to_text(raw_text=raw_text)
        subs = get_time_steps(res, user_input)
        return {"res": res, "subs": subs}
    except Exception as e:
        return {"error": f"{type(e)}: {e}"}


@app.route('/getfile', methods=['GET', 'POST'])
def getfile():
    if request.method == 'POST':

        file = request.files['myfile']
        filename = secure_filename(file.filename)
        file.save(os.path.join("logs", filename))

        with open(os.path.join("logs", filename)) as f:
            file_content = f.read()

        res = apply_punkt_to_text(raw_text=file_content)
        return res

    else:
        res = request.args['myfile']
    return res


def save_log(txt):
    timestamp = time.strftime('%Y-%m-%d %H-%M-%S')
    with open(f"./logs/log-{timestamp}.txt", "w", encoding="utf-8") as writer:
        writer.write(txt)


if __name__ == '__main__':
    # test = apply_punkt_to_text(raw_text="что это спросил он как это понимать")
    port = os.environ.get('PORT')
    if port:
        # 'PORT' variable exists - running on Heroku, listen on external IP and on given by Heroku port
        app.run(host='0.0.0.0', port=int(port))

    else:
        # 'PORT' variable doesn't exist, running not on Heroku, presumably running locally, run with default
        #   values for Flask (listening only on localhost on default Flask port)
        app.run()
