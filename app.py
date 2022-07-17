from flask import Flask, session, render_template, abort, request, redirect, flash
from datetime import datetime

from findnames import find_names
from functions import create_user_dir, get_excel_files_by_user

import os

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'


AbsPath = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(AbsPath, "static", "users")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/home')
def index():  # put application's code here

    create_user_dir(app.config["UPLOAD_FOLDER"])

    return render_template(
        "index.html",
        title="Home",
        year=datetime.now().year
    )

@app.route('/find/names', methods=["GET", "POST"])
def findnames():

    create_user_dir(app.config["UPLOAD_FOLDER"])

    input_files, output_files = get_excel_files_by_user(app.config["UPLOAD_FOLDER"])

    #print(os.listdir("~/static/users/input"))

    if request.method == "POST":

        if request.files["excelfile"].filename != "":

            excelfile = request.files["excelfile"]

            inputfilepath = os.path.join(app.config["UPLOAD_FOLDER"], os.getlogin(), "input", excelfile.filename)
            outputfilepath = os.path.join(app.config["UPLOAD_FOLDER"], os.getlogin(), "output", f"checked_{excelfile.filename}")

            downloadpath = rf"/static/users/{os.getlogin()}/output/checked_{excelfile.filename}"


            excelfile.save(inputfilepath)

            find_names(inputfilepath, outputfilepath)



            return render_template(
                "findnames.html",
                title="Find Names",
                year=datetime.now().year,
                display_error = False,
                fileuploaded = True,
                outputfilepath = downloadpath,
                input_files = input_files,
                output_files = output_files
            )

        else:
            return render_template(
                "findnames.html",
                title="Find Names",
                year=datetime.now().year,
                display_error = True,
                fileuploaded=False,
                outputfilepath=None,
                input_files=input_files,
                output_files=output_files
            )
    else:

        return render_template(
            "findnames.html",
            title="Find Names",
            year=datetime.now().year,
            display_error=False,
            input_files=input_files,
            output_files=output_files
        )

if __name__ == '__main__':
    app.run()
