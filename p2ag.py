import pandas as pd
from flask import Flask, request, redirect
from flask import url_for, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generateMain')
def generate():
    return render_template('generateMain.html')


if __name__ == '__main__':
    app.run(debug=True)
