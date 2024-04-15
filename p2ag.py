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
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file, header=None)
        columns = df.iloc[2][0:]
        # 0, 1, 2행 제거
        df = df.drop([0, 1, 2], axis=0)
        df.columns = columns
        df.reset_index(drop=True, inplace=True)
        df.fillna("", inplace=True)
        return render_template('generateConfirm.html', name=name, type=type, df=df)
    else:
        return render_template('generateMain.html', error='.xlsx 파일만 업로드 가능합니다.')


if __name__ == '__main__':
    app.run(debug=True)
