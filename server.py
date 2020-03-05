import os
from flask import Flask, request, render_template, send_from_directory, jsonify
import random

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def about():
    return render_template("about.html")

@app.route("/generate")
def generate():
    return render_template("generate.html")


@app.route("/dview")
def dview():
    return render_template("test1.html",width=400,height=600)

@app.route("/view")
def view():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    dest=None
    if(request.files.get("file")):
        upload=request.files.get("file")
        filename = upload.filename
        dest='static/input/'+filename
        upload.save(dest)
        print(dest)
    else:
        imgfilepath=request.form['imgpath']
        path,filename = os.path.split(imgfilepath)
        dest='static/input/'+filename
        print(dest)

    print("ImageFile: ",dest)

    str=" python3 p2cDemo.py "+dest
    print(str)
    import subprocess
    process=subprocess.Popen(str, shell=True)
    process.wait()
    print("Program ended")

    with open('compiledwebsite.txt', 'r') as file:
        data = file.read()

    print("Printing Compiled Website")
    for line in data.splitlines():
        print(line)

    return render_template("generate.html",inpimg=dest,pcode=data,hfname=filename)

if __name__ == "__main__":
    app.run(debug=True)
