from app.models import db, User
from app.package import get_sha1
user = User(open_id='oyab15UR9j5BbTtj_sKKMHNEtSSw', union_id='oy9ft0RKmgFXI_K8NFZYSY6CjnIA',
    session_key='sdkBgQyQyFjUFpf2zjjrCQ==', session_id='9d332e5f6f0eb60deb4a05b1968b071a1bac0da4')
db.session.add(user)
db.session.commit()

User.query.filter_by(session_id='9d332e5f6f0eb60deb4a05b1968b071a1bac0da4').first()

