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
    # 개인정보 보호책임자(담당부서)
    chargeName = request.form['chargeName']
    chargeAffiliation = request.form['chargeAffiliation']
    chargePhone = request.form['chargePhone']
    chargeEmail = request.form['chargeEmail']
    chargeEtc = request.form['chargeEtc']
    # 개인정보의 열람청구를 접수/처리하는 부서
    department = request.form['department']
    departmentName = request.form['departmentName']
    departmentPhone = request.form['departmentPhone']
    departmentEmail = request.form['departmentEmail']
    departmentEtc = request.form['departmentEtc']

    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file, header=None)
        columns = df.iloc[2][0:]
        # 0, 1, 2행 제거
        df = df.drop([0, 1, 2], axis=0)
        df.columns = columns
        df.reset_index(drop=True, inplace=True)
        df.fillna("", inplace=True)
        return render_template('generateConfirm.html', name=name, type=type, df=df, chargeName=chargeName,
                               chargeAffiliation=chargeAffiliation, chargePhone=chargePhone, chargeEmail=chargeEmail,
                               chargeEtc=chargeEtc, department=department, departmentName=departmentName,
                               departmentPhone=departmentPhone, departmentEmail=departmentEmail,
                               departmentEtc=departmentEtc)
    else:
        return render_template('generateMain.html', error='.xlsx 파일만 업로드 가능합니다.')


if __name__ == '__main__':
    app.run(debug=True)
