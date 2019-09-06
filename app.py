from flask import Flask, render_template, redirect
from read import read, get_json
from json import loads
import os




app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/status/')
def status():
    a = read('status')
    a = list(map(lambda x: x.split('~'), a))
    return render_template("status.html", content=a)

@app.route('/problemset/<num>/')
def problemset(num):
    content = get_json(f"problems/{num}/cfg.json")
    # print(type(content))
    return render_template("problem.html", data=content)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)