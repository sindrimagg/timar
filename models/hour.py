from extensions import db

class Hour(db.Model):
    __tablename__ = 'hours'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000))

    client = db.relationship('Client', backref='hours')
    project = db.relationship('Project', backref='hours')
