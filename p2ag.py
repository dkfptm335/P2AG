import pandas as pd
from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generateMain')
def generate():
    return render_template('generateMain.html')


@app.route('/generateConfirm', methods=['POST'])
def generateConfirm():
    name = request.form['name']
    type = request.form['type']
    file = request.files['file']
    df = pd.read_excel(file)
    return render_template('generateConfirm.html', name=name, type=type, df=df)


if __name__ == '__main__':
    app.run(debug=True)
