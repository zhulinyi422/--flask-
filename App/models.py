from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    s_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    s_name = db.Column(db.String(16),unique=True)
    s_age = db.Column(db.Integer,default=16)
    grades = db.Column(db.Integer,db.ForeignKey('grade.g_id'))
    __tablename__ = 'student'


class Grade(db.Model):
    g_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    g_name = db.Column(db.String(16),unique=True)
    g_create_time = db.Column(db.DateTime,default=datetime.now())
    students = db.relationship('Student',backref='grade')
    __tablename__ = 'grade'

class User(db.Model):
    u_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    u_name = db.Column(db.String(16),autoincrement=True,unique=True)
    password = db.Column(db.String(200))
    roles = db.Column(db.Integer,db.ForeignKey('role.r_id'),nullable=True)
    __tablename__ = 'user'

class Role(db.Model):
    r_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    r_name = db.Column(db.String(20),unique=True)
    users = db.relationship('User',backref='role')
    __tablename__ = 'role'

    def save(self):
        db.session.add(self)
        db.session.commit()

rp = db.Table('rp',
              db.Column('r_id',db.Integer,db.ForeignKey('role.r_id'),primary_key=True),
              db.Column('p_id',db.Integer,db.ForeignKey('permission.p_id'),primary_key=True)
              )

class Permission(db.Model):
    p_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    p_name = db.Column(db.String(20),unique=True)
    roles = db.relationship('Role',secondary=rp, backref='permission')
    __tablename__ = 'permission'