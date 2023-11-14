from ..utils import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fullName = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    businessEmail = db.Column(db.String(), unique=True, nullable=False)
    businessName = db.Column(db.String(), unique=True, nullable=False)
    typeBusiness = db.Column(db.String(), nullable=False)
    phoneNo = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.id}')"

    def save(self):
        db.session.add(self)
        db.session.commit()
