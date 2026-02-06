from extensions import db
from sqlalchemy import UniqueConstraint

class Hour(db.Model):
    __tablename__ = 'hours'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    call = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1000))

    client = db.relationship('Client', backref='hours')
    project = db.relationship('Project', backref='hours')

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    __table_args__ = (
        UniqueConstraint('client_id', 'description', name='uq_client_description'),
    )
    client = db.relationship('Client', backref='projects')

