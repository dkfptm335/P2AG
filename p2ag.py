from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
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
