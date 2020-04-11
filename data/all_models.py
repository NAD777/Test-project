import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Problem(SqlAlchemyBase):
    __tablename__ = 'problems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(255), unique=False, nullable=False)
    memory = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    difficulty = sqlalchemy.Column(sqlalchemy.Integer, unique=False, nullable=False)
    condition = sqlalchemy.Column(sqlalchemy.Text(), unique=False, nullable=False)
    inp = sqlalchemy.Column(sqlalchemy.Text(), unique=False, nullable=False)
    output = sqlalchemy.Column(sqlalchemy.Text(), unique=False, nullable=False)
    col_examples = sqlalchemy.Column(sqlalchemy.Integer(), unique=False, nullable=False, default=2)

    def __repr__(self):
        return '<Problem {} {}>'.format(self.id, self.name)


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    packages = orm.relation("Packages", back_populates='user')

    role = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    def __repr__(self):
        return f"<User> {self.id} {self.nickname} {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Packages(SqlAlchemyBase):
    __tablename__ = 'packages'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_name = sqlalchemy.Column(sqlalchemy.String(255), unique=False, nullable=False)
    problem = sqlalchemy.Column(sqlalchemy.String(255), unique=False, nullable=False)
    lan = sqlalchemy.Column(sqlalchemy.String(255), unique=False, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String(255), unique=False, nullable=False)
    code = sqlalchemy.Column(sqlalchemy.String(), unique=False, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    def __repr__(self):
        return '<Package {} {} {}>'.format(self.id, self.user_name, self.status)

    def __str__(self):
        return '<Package {} {} {}>\n{}'.format(self.id, self.user_name, self.status, self.code)


