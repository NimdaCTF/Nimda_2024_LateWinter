from core import config
from source.logic import Task
from flask import Flask, request, render_template, session, redirect
from os import urandom
from source.utils import generate_flag
from time import sleep

app = Flask(__name__)
app.secret_key = urandom(256)
answer = None


@app.route('/', methods=['GET'])
def on_root():
    session['solved'] = False
    return render_template('index.html',
                           C1=config['task']['c'][0],
                           C2=config['task']['c'][1],
                           C3=config['task']['c'][2],
                           C4=config['task']['c'][3],
                           D1=config['task']['d'][0],
                           D2=config['task']['d'][1],
                           D3=config['task']['d'][2],
                           D4=config['task']['d'][3],
                           D5=config['task']['d'][4],
                           D6=config['task']['d'][5],
                           D7=config['task']['d'][6],
                           D8=config['task']['d'][7],
                           R_MIN=config['task']['r'][0],
                           R_MAX=config['task']['r'][1]
                           )


@app.route('/flag', methods=['GET'])
def on_flag():
    if session.get('solved', False) is True:
        if not request.cookies.get('id'):
            return 'Bad Id, contact CTF admin', 424
        return render_template('flag.html', FLAG=generate_flag(request.cookies['id']))
    else:
        return render_template('flag.html', FLAG='Solve it first :^)')


@app.route('/', methods=['POST'])
def on_root_post():
    global answer
    if not request.json.get('answer'):
        return 'No', 400

    local_ans = request.json['answer']
    if not isinstance(local_ans, str):
        return 'No', 400

    local_ans = local_ans.replace(' ', '').upper()


    answer = '3C2+4C2+3C3+2C3+2C2+2C4+8C2+</>+6C4'
    # if answer is None:
    #     for i in range(*config['task']['r']):
    #         t = Task(i)
    #         res = t.calculate(8)

    #         if answer is None:
    #             answer = res
    #         elif answer[0] > res[0]:
    #             answer = res
    #     print(answer[0])
    #     print(answer[1])

    # sleep(10)  # No brute-force xd

    if local_ans == answer:
        session['solved'] = True
        return 'Ok', 200

    return 'No', 400


if __name__ == '__main__':
    app.run(debug=True)
