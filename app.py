from flask import Flask, render_template, redirect
from read import read 


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/status/')
def status():
    a = read('status')
    a = list(map(lambda x: x.split('~'), a))
    return render_template("status.html", content=a)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)