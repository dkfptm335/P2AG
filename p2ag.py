import requests
from flask import Flask, request, redirect
from flask import url_for, render_template
import pandas as pd

app = Flask(__name__)
app.secret_key = 'random string'

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
email = []

for result in data['results']:
    if result['properties']['id']['title']:
        id.append(result['properties']['id']['title'][0]['plain_text'])
    if result['properties']['pw']['rich_text']:
        pw.append(result['properties']['pw']['rich_text'][0]['plain_text'])
    if result['properties']['name']['rich_text']:
        name.append(result['properties']['name']['rich_text'][0]['plain_text'])
    if result['properties']['email']['rich_text']:
        email.append(result['properties']['email']['rich_text'][0]['plain_text'])

df = pd.DataFrame(zip(id, pw, name, email), columns=['id', 'pw', 'name', 'email'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main', methods=['POST'])
def main():
    userId = request.form['userId']
    userPw = request.form['userPw']

    if userId in df['id'].values:
        if userPw == df[df['id'] == userId]['pw'].values[0]:
            return render_template('main.html', userId=userId, userPw=userPw,
                                   userName=df[df['id'] == userId]['name'].values[0], userGender=df[df['id'] == userId])
        else:
            return "비밀번호가 일치하지 않습니다."


@app.route('/signUp', methods=['POST'])
def signUp():
    userNewId = request.form['userNewId']
    userNewPw = request.form['userNewPw']
    userNewPw2 = request.form['userNewPw2']
    userNewName = request.form['userNewName']
    userNewEmail = request.form['userNewEmail']

    if userNewId in df['id'].values:
        return render_template('duplicatedId.html')
    elif userNewEmail in df['email'].values:
        return render_template('duplicatedEmail.html')
    elif userNewPw != userNewPw2:
        return render_template('notMatch.html')
    else:
        return render_template('signUp.html', userNewId=userNewId, userNewPw=userNewPw,
                               userNewName=userNewName, userNewEmail=userNewEmail)


@app.route('/submitSelection', methods=['POST'])
def submitSelection():
    selection = request.form['selection']
    if selection == 'university':
        return redirect(url_for('univForm'))


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
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # file = request.files['file']
    data = pd.read_excel(file)
    return render_template('univResult.html', provider=provider, date=date, policy=policy,
                           email=email, name=name, birthday=birthday, optional_info=optional_info,
                           tables=[data.to_html(classes='data')], titles=data.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
