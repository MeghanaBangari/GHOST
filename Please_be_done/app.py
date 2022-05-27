from flask import Flask, request
from flask import render_template
from hideText import hideFunc, revealFunc

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main")
def main():
    return render_template("index.html")


@app.route("/image")
def image():
    return render_template("demo.html")


@app.route("/text")
def text():
    return render_template("text.html")


@app.route("/hide", methods=['POST', 'GET'])
def hide():
    formInfo = request.form
    result = hideFunc(formInfo['sec_msg'],
                      formInfo['psw'], formInfo['cvr_msg'])
    return render_template("text.html", result=result)


@app.route("/reveal", methods=['POST', 'GET'])
def reveal():
    formInfo = request.form
    result_reveal = revealFunc(formInfo['steg_msg'], formInfo['psw_rev'])
    return render_template("text.html", result_reveal=result_reveal)


if __name__ == '__main__':
    app.run(debug=True)
