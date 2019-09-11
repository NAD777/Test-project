from flask import Flask, render_template, redirect, request
from read import string_to_dict
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
    problem = db.Column(db.String(255), unique=False, nullable=False)
    lan = db.Column(db.String(255), unique=False, nullable=False)
    status = db.Column(db.String(255), unique=False, nullable=False)

    def __repr__(self):
        return '<Status {} {} {} {}>'.format(self.id, self.name, self.status)


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
    task = Status(name="AU", status="Ok")
    
    db.session.add(task)
    db.session.commit()
    print(task.id)
    return redirect("/")


@app.route('/status/')
def status():
    arr = Status.query.all()
    content = [(el.id, el.name, el.problem, el.lan, el.status) for el in reversed(arr)]
    return render_template("status.html", content=content)


@app.route("/problemset/list/<num>/")
def problemset(num):
    n = int(num)
    print(Problem.query.all())
    arr = Problem.query.all()[(n - 1) * COL_PROBLEMS_ONE_PAGE:n * COL_PROBLEMS_ONE_PAGE]
    content = [(el.id, el.name, el.difficulty) for el in arr]
    return render_template("problemset.html", content_table=content)


@app.route('/problemset/<num>/', methods=['POST', 'GET'])
def problemset_num(num):
    n = int(num)
    if request.method == 'GET':
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
        # print(request.form['textarea'])
        lan = request.form['lan']
        name = request.form['name']
        status = Status(name=name, status="comp", problem=num, lan=lan)
        db.session.add(status)
        db.session.commit()
        id_status = status.id
        problem = Problem.query.filter_by(id=n).first()
        test = Test(tl_time=problem.time, ml_memory=problem.memory)
        # TODO: REFACTOR THIS PART OF CODE
        if lan == "cpp":
            test.create_file(request.form["textarea"], f'source/{id_status}.cpp')
            if test.compile_С(f"source/{id_status}.cpp", f"programms/{id_status}"):
                status = Status.query.filter_by(id=id_status).first()
                status.status = "run"
                db.session.commit()
            else:
                status = Status.query.filter_by(id=id_status).first()
                status.status = "ce"
                test.delete_file(f"source/{id_status}.cpp")
                db.session.commit()
                return redirect('/status/')
            ans = test.run_all_tests(f"problems/{n}/tests/", f"programms/{id_status}")
            status = Status.query.filter_by(id=id_status).first()
            if not ans:
                status.status = "ac"
                db.session.commit()
            else:
                status.status = f"{ans[0]} {ans[1]}"
                db.session.commit()
            test.delete_file(f"source/{id_status}.cpp")
            test.delete_file(f"programms/{id_status}")
        elif lan == "pas":
            test.create_file(request.form["textarea"], f'source/{id_status}.pas')
            if test.compile_pas(f"source/{id_status}.pas", f"programms/{id_status}"):
                status = Status.query.filter_by(id=id_status).first()
                status.status = "run"
                db.session.commit()
            else:
                status = Status.query.filter_by(id=id_status).first()
                status.status = "ce"
                test.delete_file(f"source/{id_status}.pas")
                db.session.commit()
                return redirect('/status/')
            ans = test.run_all_tests(f"problems/{n}/tests/", f"programms/{id_status}")
            status = Status.query.filter_by(id=id_status).first()
            print(ans)
            if not ans:
                status.status = "ac"
                db.session.commit()
            else:
                status.status = f"{ans[0]} {ans[1]}"
                db.session.commit()
            test.delete_file(f"source/{id_status}.pas")
            test.delete_file(f"programms/{id_status}")
            test.delete_file(f'programms/{id_status}.o')
        #####################################################
        return redirect('/status/')


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
