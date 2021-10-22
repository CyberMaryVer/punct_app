import os
import time
from flask import Flask, request, render_template
from punct import apply_punkt_to_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1024
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
        user_input = request.args.get("text", None)
        res = apply_punkt_to_text(raw_text=user_input)
        return {"punct": res}
    except Exception as e:
        return {"error": f"{type(e)}: {e}"}


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