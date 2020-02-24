from cfc import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, nullable = True)
    netid = db.Column(db.String(20),nullable = True)
    first_name = db.Column(db.String(30), unique = False, nullable = False)
    last_name = db.Column(db.String(30), unique = False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    image = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    major = db.Column(db.String(20), nullable = False)
    type_id = db.Column(db.String(20), nullable = True)
    ref = db.relationship('RefList', backref = 'Referer', lazy = True)

    def __repr__(self):
        return "Id:{} First Name:{} Last Name:{} Email:{}".format(self.id,self.first_name,self.last_name,self.email)




class RefList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    job_title = db.Column(db.String(30), nullable = False)
    job_des = db.Column(db.Text, nullable = False)
    company = db.Column(db.String(100), nullable=False)
    ref_id = db.Column(db.Integer, db.ForeignKey('user.netid'), nullable=False)
    status = db.Column(db.String(5), nullable = False, default = 'open')

    def __repr__(self):
        return "Job Title : {} Company: {} Status: {} ref id : {}".format(self.job_title,self.company,self.status,self.ref_id)


db.create_all()
db.session.commit()