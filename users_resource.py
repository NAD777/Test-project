from flask import abort, jsonify
from flask_restful import Resource
from data.db_session import create_session
from data.all_models import User, Packages


def abort_if_users_not_found(user_name):
    session = create_session()
    user = session.query(User).filter(User.nickname == user_name).first()
    if not user:
        abort(404, message=f"User {user_name} not found")


class UsersResource(Resource):
    def get(self, user_name):
        abort_if_users_not_found(user_name)
        session = create_session()
        user = session.query(User).filter(User.nickname == user_name).first()

        accepted = session.query(Packages).filter(Packages.user_id == user.id, Packages.status == 'ac').all()
        ids_accept = set(map(lambda x: int(x.problem), accepted))

        wa = session.query(Packages).filter(Packages.user_id == user.id, Packages.status.like('WA%')).all()
        ids_wa = list(map(lambda x: int(x.problem), wa))

        ml = session.query(Packages).filter(Packages.user_id == user.id, Packages.status.like('ML%')).all()
        ids_ml = list(map(lambda x: int(x.problem), ml))

        tl = session.query(Packages).filter(Packages.user_id == user.id, Packages.status.like('TL%')).all()
        ids_tl = list(map(lambda x: int(x.problem), tl))

        ce = session.query(Packages).filter(Packages.user_id == user.id, Packages.status == 'ce').all()
        ids_ce = list(map(lambda x: int(x.problem), ce))
        
        all_exceptions = (set(ids_wa) | set(ids_ml) | set(ids_tl) | set(ids_ce)) ^ ids_accept

        nickname = user.nickname
        email = user.email
        role = user.role

        return jsonify({'user': {"nickname": nickname,
                                 "email": email, "role": role,
                                 "accepted": [el for el in sorted(ids_accept)],
                                 "wrong answer": len(ids_wa),
                                 "memory limit": len(ids_ml),
                                 "time limit": len(ids_tl),
                                 "compilation error": len(ids_ce),
                                 "not done": [el for el in sorted(all_exceptions)]}})
