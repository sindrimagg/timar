from flask import Flask, url_for, redirect
from extensions import db
from routes import clients_bp, projects_bp, hours_bp, forms_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time_tracker.db'
app.config['SECRET_KEY'] = 'dev-secret'

db.init_app(app)

app.register_blueprint(clients_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(hours_bp)
app.register_blueprint(forms_bp)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('hours.hours'))

app.run(debug=True, host="0.0.0.0", port="5001")
