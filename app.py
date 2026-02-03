from flask import Flask
from extensions import db
from routes import clients_bp, projects_bp, hours_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time_tracker.db'
app.config['SECRET_KEY'] = 'dev-secret'

db.init_app(app)

app.register_blueprint(clients_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(hours_bp)

with app.app_context():
    db.create_all()

app.run(debug=True)
