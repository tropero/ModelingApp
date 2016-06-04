import os
from flask import Flask, request, redirect, url_for

from flask.templating import render_template
import generator as gg
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:\\Users\\Krzychu\\Dropbox\\ModelingApp\\uploads\\'
ALLOWED_EXTENSIONS = set(['graphml'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    datalist = gg.generate()
    return render_template("index.html", N=datalist[0], K=datalist[1], avgdegree=datalist[2],
                           diam=datalist[3], tran=datalist[4], avgcl=datalist[5],
                           stddev=datalist[6])
    # return render_template("index.html", N=gg.generate()[0], K=gg.generate()[1], avgdegree=gg.generate()[2],
    #                        diam=gg.generate()[3], tran=gg.generate()[4], avgcl=gg.generate()[5],
    #                        stddev=gg.generate()[6])


@app.route("/generate")
def generate():
    return render_template("getData.html")

@app.route('/xxx', methods=['POST'])
def test():
    if request.method == 'POST':
        model = request.form['model']
        return "model to: "+model
    #                    request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #
    # error = 'Invalid username/password'
    #     # if valid_login(request.form['username'],
    #     #                request.form['password']):
    #     #     return log_the_user_in(request.form['username'])
    #     # else:
    #     #     error = 'Invalid username/password'
    # # the code below is executed if the request method
    # # was GET or the credentials were invalid
    # return render_template('login.html', error=error)


@app.route("/uploaded")
def uploaded():
    return """
    <!doctype html>
    Uploaded files: <br />
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'], ))


@app.route("/upload", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'], ))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=7777)

    # do poprawy:
    # opracować sposób do podawania parametrów i modelowania roznych topologii, czy to scale free czy np. scentralizowanych
    # podawać parametr i otrzymywać topologie -> z nich wyliczać jakieś dane charakterystycze
    # zrobić również ewolucję botnetów z paskiem, aby obserwować jak one się dodają do siebie podczas przesuwania paska
