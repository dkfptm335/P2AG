import pandas as pd
import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main', methods=['POST'])
def main():
    userId = request.form['userId']
    userPw = request.form['userPw']

    token = r'secret_DMk5aGpHhepTCDPLnpslUaxNFIL5Az2sAGi23PI7rdR'
    database_id = r'031db1df89214a38bbf9302803d5c5b6'
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    url = f'https://api.notion.com/v1/databases/{database_id}/query'

    data = requests.post(url, headers=headers).json()

    id = []
    pw = []
    name = []
    gender = []

    for result in data['results']:
        if result['properties']['id']['title']:
            id.append(result['properties']['id']['title'][0]['plain_text'])
        if result['properties']['pw']['rich_text']:
            pw.append(result['properties']['pw']['rich_text'][0]['plain_text'])
        if result['properties']['name']['rich_text']:
            name.append(result['properties']['name']['rich_text'][0]['plain_text'])
        if result['properties']['gender']['rich_text']:
            gender.append(result['properties']['gender']['rich_text'][0]['plain_text'])

    df = pd.DataFrame(zip(id, pw, name, gender), columns=['id', 'pw', 'name', 'gender'])

    if userId in df['id'].values:
        if userPw == df[df['id'] == userId]['pw'].values[0]:
            return render_template('main.html', userId=userId, userPw=userPw, userName=df[df['id'] == userId]['name'].values[0], userGender=df[df['id'] == userId])
        else:
            return "비밀번호가 일치하지 않습니다."


@app.route('/univForm')
def univForm():
    return render_template('univForm.html')


@app.route('/univResult', methods=['POST'])
def univResult():
    provider = request.form.get('provider')
    date = request.form.get('date')
    policy = request.form.get('policy')
    email = request.form.get('email')
    name = request.form.get('name')
    birthday = request.form.get('birthday')
    optional_info = request.form.get('optional_info')

    return render_template('univResult.html', provider=provider, date=date, policy=policy,
                           email=email, name=name, birthday=birthday, optional_info=optional_info)


if __name__ == '__main__':
    app.run(debug=True)
