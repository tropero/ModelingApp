import os
from flask import Flask, request, redirect, url_for

from flask.templating import render_template
import generator as gg
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'C:\\Users\\Krzychu\\PycharmProjects\\untitled20\\uploads\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return render_template("index.html", N=gg.generate()[0], K=gg.generate()[1], avgdegree=gg.generate()[2],
                           diam=gg.generate()[3], tran=gg.generate()[4], avgcl=gg.generate()[5])


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
