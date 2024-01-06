from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)


@app.route('/', methods=['GET'])
def on_root_get():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def on_root_post():
    if not request.form.get('url'):
        return 'Bad request', 400

    url = request.form['url']
    res = subprocess.check_output(f'whois {url}', shell=True)

    return res


@app.route('/afdsafdsaxaxx', methods=['GET'])
def on_flag():
    if not request.cookies.get('id'):
        return 'Rerun task, I don\'t have ur ID', 400

    res = subprocess.check_output(f'xfold {request.cookies["id"]}', shell=True)

    return res
        

if __name__ == '__main__':
    app.run(debug=True)
