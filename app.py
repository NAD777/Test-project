import json

from flask import Flask, render_template, redirect, request
from read import get_tests
from main import Test
from data.all_models import Problem, Packages, User
from data.db_session import create_session, global_init
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.forms import RegisterForm, LoginForm

COL_PROBLEMS_ONE_PAGE = 30

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeLreYUAAAAAE8DCnvD5FY0x6yEvpdYDstaj2BL'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeLreYUAAAAAMusRDSkpYeHUagVBjjI3pycTp7t'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'black'}

global_init("db/database.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)

FOR_TEST_COMPILE = 1


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("board.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter((User.email == form.login.data) | (User.nickname == form.login.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if form.password.data != form.password_repeat.data:
            return render_template('register.html',
                                   form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter((User.email == form.email.data) | (User.nickname == form.nickname.data)).first():
            return render_template('register.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            nickname=form.nickname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route("/test-problem/")
def test_problem():
    print(Problem.query.all())
    return f"{Problem.query.all()}"


@app.route("/test-add/")
def test_add():
    task = Packages(name="AU", status="Ok")

    session = create_session()
    session.add(task)
    session.commit()
    print(task.id)
    return redirect("/")


@app.route('/status/')
def status():
    session = create_session()
    arr = session.query(Packages).all()
    # print(arr)
    content = [(el.id, el.name, el.problem, el.lan, el.status) for el in reversed(arr)]
    return render_template("status.html", content=content)


@app.route("/problemset/list/<num>/")
def problemset(num):
    n = int(num)
    # print(Problem.query.all())
    session = create_session()
    arr = session.query(Problem).all()[(n - 1) * COL_PROBLEMS_ONE_PAGE:n * COL_PROBLEMS_ONE_PAGE]
    content = [(el.id, el.name, el.difficulty) for el in arr]
    return render_template("problemset.html", content_table=content)


@app.route('/problemset/<num>/', methods=['POST', 'GET'])
def problemset_num(num):
    n = int(num)
    session = create_session()
    if request.method == 'GET':
        # problem = Problem.query.filter_by(id=n).first()
        problem = session.query(Problem).filter(Problem.id == n).first()
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
            "examples": get_tests(col=int(problem.col_examples), dir=num)
        }
        return render_template("problem.html", data=content)
    elif request.method == 'POST':
        # print(request.form['textarea'])        
        lan = request.form['lan']
        name = current_user.nickname
        status = Packages(name=name, status="comp", problem=num, lan=lan, code=request.form["textarea"])
        session.add(status)
        # current_user.packages.append(status)
        # session.merge(current_user)
        session.commit()
        id_status = status.id
        print("#####!!!", id_status)
        problem = session.query(Problem).filter(Problem.id == n).first()
        test = Test(tl_time=problem.time, ml_memory=problem.memory)
        # TODO: REFACTOR THIS PART OF CODE
        if lan == "cpp":
            test.create_file(request.form["textarea"], f'source/{id_status}.cpp')
            if test.compile_С(f"source/{id_status}.cpp", f"programms/{id_status}"):
                # status = Packages.query.filter_by(id=id_status).first()
                status = session.query(Packages).filter(Packages.id == id_status).first()
                status.status = "run"
                session.commit()
            else:
                status = session.query(Packages).filter(Packages.id == id_status).first()
                status.status = "ce"
                test.delete_file(f"source/{id_status}.cpp")
                session.commit()
                return redirect('/status/')
            ans = test.run_all_tests(f"problems/{n}/tests/", f"programms/{id_status}")
            status = session.query(Packages).filter(Packages.id == id_status).first()
            if not ans:
                status.status = "ac"
                session.commit()
            else:
                status.status = f"{ans[0]} {ans[1]}"
                session.commit()
            test.delete_file(f"source/{id_status}.cpp")
            test.delete_file(f"programms/{id_status}")
        elif lan == "pas":
            test.create_file(request.form["textarea"], f'source/{id_status}.pas')
            if test.compile_pas(f"source/{id_status}.pas", f"programms/{id_status}"):
                status = session.query(Packages).filter(Packages.id == id_status).first()
                status.status = "run"
                session.commit()
            else:
                status = session.query(Packages).filter(Packages.id == id_status).first()
                status.status = "ce"
                test.delete_file(f"source/{id_status}.pas")
                session.commit()
                return redirect('/status/')
            ans = test.run_all_tests(f"problems/{n}/tests/", f"programms/{id_status}")
            status = session.query(Packages).filter(Packages.id == id_status).first()
            print(ans)
            if not ans:
                status.status = "ac"
                session.commit()
            else:
                status.status = f"{ans[0]} {ans[1]}"
                session.commit()
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
        # examples = request.form['examples'].replace("\r\n", '~')
        prm = Problem(name=name, memory=int(memory), time=int(time),
                      difficulty=int(difficulty), condition=condition, inp=inp,
                      output=output)
        session = create_session()
        session.add(prm)
        session.commit()
        return redirect("/add/")


@app.route("/solution/<num>/")
def solution(num):
    n = int(num)
    session = create_session()
    # solution = Packages.query.filter_by(id=n).first()
    solution = session.query(Packages).filter(Packages.id == n).first()
    if solution.code is None:
        code = 'None'
    else:
        code = solution.code
    print(code)
    content = (solution.id, solution.name, solution.problem, solution.lan, solution.status, code)
    return render_template("solution.html", content=content)


@app.route('/status_reload', methods=['POST'])
def status_reload():
    data = json.loads(request.data)  # idшники
    # TODO: В массиве записаны id статусов, которые нужно достать из БД
    #  и затем вернуть из функции список [{'id': id, 'status': status}, ...] закодированный в json
    session = create_session()
    data = data['id']
    response = {'data': []}
    for id_pos in data:
        a = {
            'id': str(id_pos),
            'status': str(session.query(Packages).filter(Packages.id == int(id_pos)).first().status)
        }
        response['data'].append(a)
        # return json.dumps({'data': [{'id': '75', 'status': 'ac'}, {'id': '73', 'status': 'WA'}]})  # пример
    print(response)
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=40000)
