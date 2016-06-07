import os
from flask import Flask, request, redirect, url_for
import json
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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print("key")
        print(request.get_data())
        model = request.form['model']
        print("key")

        print(type(model))

        if model == "1":
            given_data_dict = {'number_of_nodes': '', 'number_of_edges': '', 'seed': ''}

            print("model 1")
            model = request.form['model']
            if request.form['number_of_nodes'] is not '':
                number_of_nodes = request.form['number_of_nodes']
                given_data_dict['number_of_nodes'] = int(number_of_nodes)
            else:
                number_of_nodes = 666

            if request.form['number_of_edges'] is not '':
                number_of_edges = request.form['number_of_edges']
                given_data_dict['number_of_edges'] = int(number_of_edges)
            else:
                number_of_edges = 666

            if request.form['seed'] is not '':
                seed = request.form['seed']
                given_data_dict['seed'] = int(seed)
            else:
                given_data_dict['seed'] = None

            print("dla 1 dict:")
            print(given_data_dict)

        elif model == "2":
            print("model 2")
            given_data_dict = {'number_of_nodes': '', 'number_of_neighbors': '', 'propability': '', 'seed': ''}

            if request.form['number_of_nodes'] is not '':
                number_of_nodes = request.form['number_of_nodes']
                given_data_dict['number_of_nodes'] = int(number_of_nodes)

            else:
                number_of_nodes = 666

            if request.form['number_of_neighbors'] is not '':
                number_of_neighbors = request.form['number_of_neighbors']
                given_data_dict['number_of_neighbors'] = int(number_of_neighbors)

            else:
                number_of_neighbors = 666

            if request.form['propability'] is not '':
                propability = request.form['propability']
                given_data_dict['propability'] = float(propability)

            else:
                propability = 666

            if request.form['seed'] is not '':
                seed = request.form['seed']
                given_data_dict['seed'] = int(seed)
            else:
                seed = 666
            print("dla 2 dict:")
            print(given_data_dict)

        elif model == "3":
            given_data_dict = {'number_of_nodes': '', 'propability': '', 'seed': ''}

            print("model 3")
            if request.form['number_of_nodes'] is not '':
                number_of_nodes = request.form['number_of_nodes']
                given_data_dict['number_of_nodes'] = int(number_of_nodes)

            else:
                number_of_nodes = 666

            if request.form['propability'] is not '':
                propability = request.form['propability']
                given_data_dict['propability'] = float(propability)

            else:
                propability = 666

            if request.form['seed'] is not '':
                seed = request.form['seed']
                given_data_dict['seed'] = int(seed)
            else:
                seed = 666
            print("dla 3 dict:")
            print(given_data_dict)

        datalist = gg.generate(model, given_data_dict)



    else:
        model = "1"
        given_data_dict = {'number_of_nodes': 10, 'number_of_edges': 3, 'seed': ''}
        datalist = gg.generate(model, given_data_dict)
    # model = 1
    return render_template("index.html", mod=model, N=datalist[0], K=datalist[1], avgdegree=datalist[2],
                           diam=datalist[3], tran=datalist[4], avgcl=datalist[5],
                           stddev=datalist[6])
    # return render_template("index.html", N=gg.generate()[0], K=gg.generate()[1], avgdegree=gg.generate()[2],
    #                        diam=gg.generate()[3], tran=gg.generate()[4], avgcl=gg.generate()[5],
    #                        stddev=gg.generate()[6])


@app.route("/generate")
def generate():
    return render_template("getData.html")



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

