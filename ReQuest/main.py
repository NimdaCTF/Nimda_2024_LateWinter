from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def on_root():
    if not request.cookies.get('id'):
        return 'Contact CTF Admin', 424

    content = f'''Твой UserID:{request.cookies['id']}<br>nc nimda.icyftl.ru 1111'''

    return render_template_string('''
    <html>
    <head>
        <style type="text/css">
            html, body {
                height : 100%;
                width : 100%;
                overflow : hidden;
            }
            .wrapper {
                height : 100%;
                width : 100%;
                padding: 20px;
            }
            .content {
                height : 100%;
                width : 100%;
            }
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="content">''' + content + '''</div>
        </div>
    </body>
</html>''')


if __name__ == '__main__':
    app.run()
