from app import db
from datetime import datetime, date

class Users(db.Model):
    __tablename__ = "users"
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.username}"


class KanBanList(db.Model):
    __tablename__ = "kanbanlist"
    sno = db.Column(db.ForeignKey("users.sno"))
    sid = db.Column(db.Integer, primary_key=True)
    listName = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.listName}"


class ListItems(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.ForeignKey("kanbanlist.sid"))
    title = db.Column(db.String(200), nullable=False)
    reference = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    completedFlag = db.Column(db.String(20), nullable=False, default="off")
    timeCreated = db.Column(db.String(20), default=str(datetime.now()))
    timeCompleted = db.Column(db.String(20))
    username = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.title}"