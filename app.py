from flask import Flask, render_template, redirect, request
from read import read, string_to_dict
from flask_sqlalchemy import SQLAlchemy
from main import Test


COL_PROBLEMS_ONE_PAGE = 10


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    memory = db.Column(db.Integer, unique=False, nullable=False)
    time = db.Column(db.Integer, unique=False, nullable=False)
    difficulty = db.Column(db.Integer, unique=False, nullable=False)
    condition = db.Column(db.Text(), unique=False, nullable=False)
    inp = db.Column(db.Text(), unique=False, nullable=False)
    output = db.Column(db.Text(), unique=False, nullable=False)
    examples = db.Column(db.Text(), unique=False, nullable=False)  # rasparse

    def __repr__(self):
        return '<Problem {} {}>'.format(self.id, self.name)


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return '<Status {} {}>'.format(self.id, self.n, self.name, self.status)


db.create_all()

FOR_TEST_COMPILE = 1

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/test-problem/")
def test_problem():
    print(Problem.query.all())
    return f"{Problem.query.all()}"


@app.route("/test-add/")
def test_add():
    task = Problem(name='A + B',
                    memory=16,
                    time=1,
                    difficulty=1,
                    condition='А + B',
                    inp="Два числа",
                    output="Сумма двух чисел",
                    examples="1 2~3|3 4~7"
                    ) 
    db.session.add(task)
    db.session.commit()
    return redirect("/")


@app.route('/status/')
def status():
    a = read('status')
    a = list(map(lambda x: x.split('~'), a))
    return render_template("status.html", content=a)


@app.route("/problemset/list/<num>/")
def problemset(num):
    n = int(num)
    print(Problem.query.all())
    arr = Problem.query.all()[(n - 1) * COL_PROBLEMS_ONE_PAGE:n * COL_PROBLEMS_ONE_PAGE]
    content = [(el.id, el.name, el.difficulty) for el in arr]
    return render_template("problemset.html", content_table=content)


@app.route('/problemset/<num>/', methods=['POST', 'GET'])
def problemset_num(num):
    if request.method == 'GET':
        n = int(num)
        problem = Problem.query.filter_by(id=n).first()
        # content = get_json(f"problems/{num}/cfg.json")
        # print(type(content))
        content = {
            "name": problem.name,
            "mem": problem.memory,
            "time": problem.time,
            "difficulty": problem.difficulty,
            "condition": problem.condition,
            "inp": problem.inp,
            "output": problem.output,
            "examples":  string_to_dict(problem.examples)
        }
        return render_template("problem.html", data=content)
    elif request.method == 'POST':
        print(request.form['textarea'])
        print(request.form['lan'])
        test = Test()
        if request.form['lan'] == "CPP":
            test.create_file(request.form["textarea"], f'source/{FOR_TEST_COMPILE}.cpp')
            print(test.compile_С(f"source/{FOR_TEST_COMPILE}.cpp", f"programms/{FOR_TEST_COMPILE}"))
            print(test.run_all_tests(f"problems/1/tests/", f"programms/{FOR_TEST_COMPILE}"))
        return redirect(f'/problemset/{num}/')


@app.route('/add/', methods=["POST", 'GET'])
def add():
    if request.method == 'GET':
        return render_template("add.html")
    elif request.method == 'POST':
        name = request.form['name']
        memory = request.form['mem']
        time = request.form['time']
        difficulty = request.form['difficulty']
        condition = request.form['condition']
        inp = request.form['input']
        output = request.form['output']
        examples = request.form['examples'].replace("\r\n", '~')
        prm = Problem(name=name, memory=int(memory), time=int(time),
            difficulty=int(difficulty), condition=condition, inp=inp,
             output=output, examples=examples)
        db.session.add(prm)
        db.session.commit()
        return redirect("/add/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10001)
