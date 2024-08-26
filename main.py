from flask import Flask, render_template, request, Response, redirect, send_from_directory, url_for
import os
import uuid
from pypil import rotation_func
from werkzeug.utils import secure_filename
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(_basedir, 'downloads')

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET": 
        return render_template("index.html")
    elif request.method == "POST":
        return "Success"


@app.route("/edit_file", methods=['POST'])
def edit_file():
    file = request.files['uploadedFile']
    file_ext = file.filename.split(".")[1]
    rotation = int(request.form['integerValue'])

    if file.mimetype not in ['image/jpeg', 'image/png', 'image/jpg']:
        return "Only JPEG and PNG files are allowed", 400

    file_uuid_name = secure_filename(f"{file.filename}{uuid.uuid4()}.{file_ext}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_uuid_name)
    file.save(file_path)

    rotation_func(file_path, rotation)
    return redirect(f"/download/{file_uuid_name}/{file_ext}")


@app.route("/download/<filename>/<extn>")
def download(filename, extn):
    return send_from_directory("downloads", filename, download_name=f"result.{extn}")



if __name__ == "__main__": 
    app.run(debug=True)