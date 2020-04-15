import json

from flask import Flask, render_template, redirect, request, abort
from read import get_tests, remove_folder
from main import Test
from data.all_models import Problem, Packages, User
from data.db_session import create_session, global_init
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.forms import RegisterForm, LoginForm, AddProblem
from werkzeug.utils import secure_filename
from flask_restful import Api
import users_resource

import os


COL_PROBLEMS_ONE_PAGE = 30

app = Flask(__name__)
api = Api(app)

api.add_resource(users_resource.UsersResource, '/api/users/<string:user_name>')

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


@app.route('/status/')
def status():
    session = create_session()
    arr = session.query(Packages).all()
    # print(arr)
    content = []
    for el in reversed(arr):
        user_id = el.user_id
        user_name = el.user_name
        
        content.append((el.id, user_name, el.problem, el.lan, el.status, user_id))
    return render_template("status.html", content=content)


@app.route("/problemset/list/<num>/")
def problemset(num):
    n = int(num)
    session = create_session()
    if current_user.is_authenticated:
        solved_by_user = [int(el.problem) for el in session.query(Packages).filter(Packages.user_id == current_user.id, Packages.status == 'ac').all()]
    else:
        solved_by_user = []
    arr = session.query(Problem).all()[(n - 1) * COL_PROBLEMS_ONE_PAGE:n * COL_PROBLEMS_ONE_PAGE]
    content = [(el.id, el.title, el.difficulty) for el in arr]
    return render_template("problemset.html", content_table=content, solved_by_user=solved_by_user)


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
            "id": problem.id,
            "name": problem.title,
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
        user_name = current_user.nickname
        user_id = current_user.id
        status = Packages(user_name=user_name, status="comp", problem=num, lan=lan, code=request.form["textarea"], user_id=user_id)
        session.add(status)
        session.commit()
        id_status = status.id
        print("#####!!!", id_status)
        problem = session.query(Problem).filter(Problem.id == n).first()
        test = Test(tl_time=problem.time, ml_memory=problem.memory)
        
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
        
        return redirect('/status/')


@app.route('/add/', methods=["POST", 'GET'])
@login_required
def add():
    if current_user.role == 0:
        abort(404)
    form = AddProblem()
    if form.validate_on_submit():
        title = form.title.data
        memory = form.mem.data
        time = form.time.data
        difficulty = form.difficulty.data
        condition = form.condition.data
        inp = form.inp.data
        output = form.output.data
        col_examples = form.col_examples.data
        # examples = request.form['examples'].replace("\r\n", '~')
        prm = Problem(title=title, memory=int(memory), time=int(time),
                      difficulty=int(difficulty), condition=condition, inp=inp,
                      output=output, col_examples=int(col_examples))
        session = create_session()
        session.add(prm)
        session.commit()
        prm_id = prm.id
        files = request.files.getlist(form.files.name)
        print(files)
        os.makedirs(os.path.join(f"problems/{prm_id}/tests/"))
        if files:
            for file_upload in files:
                file_name = secure_filename(file_upload.filename)
                file_content = file_upload.stream.read()
                # print(os.path.join(f"problems/{prm_id}/"))
                # file_upload.save(os.path.join(f"problems/{prm_id}/"), file_name)
                open(os.path.join(f"problems/{prm_id}/tests/", file_name), 'w').write(file_content.decode('utf-8'))
                # print(type(file_content), file_content, file_name)

        return redirect("/add/")
    return render_template("add.html", form=form, input_files=True)


@app.route('/edit/<int:num>/', methods=['POST', 'GET'])
@login_required
def edit(num):
    if current_user.role == 0:
        abort(404)
    form = AddProblem()
    session = create_session()
    problem = session.query(Problem).filter(Problem.id == num).first()
    if not problem:
        abort(404)
    if form.validate_on_submit():
        problem.title = form.title.data
        problem.memory = form.mem.data
        problem.time = form.time.data
        problem.difficulty = form.difficulty.data
        problem.condition = form.condition.data
        problem.inp = form.inp.data
        problem.output = form.output.data
        problem.col_examples = form.col_examples.data

        session.commit()
        return redirect(f"/problemset/{num}/")
    form.title.data = problem.title
    form.mem.data = problem.memory
    form.time.data = problem.time
    form.difficulty.data = problem.difficulty
    form.condition.data = problem.condition
    form.inp.data = problem.inp
    form.output.data = problem.output
    form.col_examples.data = problem.col_examples

    return render_template("add.html", form=form, input_files=False)


@app.route('/delete/<int:num>/', methods=['POST', 'GET'])
@login_required
def problem_delete(num):
    if current_user.role == 0:
        abort(404)
    session = create_session()
    problem = session.query(Problem).filter(Problem.id == num).first()
    if problem:
        session.delete(problem)
        session.commit()
        remove_folder(f"problems/{num}")
    else:
        abort(404)
    return redirect(f"/problemset/list/1/")


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
    content = (solution.id, solution.user_name, solution.problem, solution.lan, solution.status, code)
    return render_template("solution.html", content=content)


@app.route("/profile/<nickname>/")
def profile(nickname):
    session = create_session()
    profile = session.query(User).filter(User.nickname == nickname).first()
    accepted = session.query(Packages).filter(Packages.user_id == profile.id, Packages.status == 'ac').all()
    ids_accept = set(map(lambda x: int(x.problem), accepted))
    wa = session.query(Packages).filter(Packages.user_id == profile.id, Packages.status.like('WA%')).all()
    ids_wa = list(map(lambda x: int(x.problem), wa))
    ml = session.query(Packages).filter(Packages.user_id == profile.id, Packages.status.like('ML%')).all()
    ids_ml = list(map(lambda x: int(x.problem), ml))
    tl = session.query(Packages).filter(Packages.user_id == profile.id, Packages.status.like('TL%')).all()
    ids_tl = list(map(lambda x: int(x.problem), tl))
    ce = session.query(Packages).filter(Packages.user_id == profile.id, Packages.status == 'ce').all()
    ids_ce = list(map(lambda x: int(x.problem), ce))
    all_exceptions = ((set(ids_wa) | set(ids_ml) | set(ids_tl) | set(ids_ce))) - ids_accept
    print(ids_wa, wa, all_exceptions, ids_accept)
    return render_template("profile.html", profile=profile, ids_accept=ids_accept, ids_wa=ids_wa, all_exceptions=all_exceptions,
                                            ids_ml=ids_ml, ids_tl=ids_tl, ids_ce=ids_ce)


@app.route("/profile/<nickname>/all_packeges/")
def users_packeges(nickname):
    session = create_session()
    profile = session.query(User).filter(User.nickname == nickname).first()
    users_packages = session.query(Packages).filter(Packages.user_id == profile.id).all()
    content = []

    for el in reversed(users_packages):
        user_id = el.user_id
        user_name = el.user_name
        
        content.append((el.id, user_name, el.problem, el.lan, el.status, user_id))
    return render_template("status.html", content=content)


@app.route("/change_status/<nickname>")
@login_required
def change_status(nickname):
    session = create_session()
    profile = session.query(User).filter(User.nickname == nickname).first()
    if current_user.role == 1 and current_user.id != profile.id:
        profile.role = (profile.role + 1) % 2
        session.commit()
    return redirect(f"/profile/{nickname}")


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


@app.errorhandler(404)
def payme(e):
    return """<h1> Someting went wrong </h1>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=40000)
