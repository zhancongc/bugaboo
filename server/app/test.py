from app.models import db, User
from app.package import get_sha1
user = User(open_id='oyab15UR9j5BbTtj_sKKMHNEtSSw', union_id='oy9ft0RKmgFXI_K8NFZYSY6CjnIA',
    session_key='sdkBgQyQyFjUFpf2zjjrCQ==', session_id='9d332e5f6f0eb60deb4a05b1968b071a1bac0da4')
db.session.add(user)
db.session.commit()

User.query.filter_by(session_id='9d332e5f6f0eb60deb4a05b1968b071a1bac0da4').first()

from functools import wraps
def login_required(func):
    @wraps(func)
    def authenticate(*args, **kwargs):
        res = dict()
        host = request.headers.get('Host')
        if not host:
            res.update({
                'state': 0,
                'msg': 'cannot found session_id or session_id expired'
            })
            return jsonify(res)
        return func(host, *args, **kwargs)
    return authenticate


from flask import request, jsonify
@login_required
def foo(host):
    print(host)
    res = dict()
    res.update({'state': 1, 'msg': 'success'})
    return jsonify(res)

a=foo()
