"""
Simple Time Tracker - single-file Flask app (FIXED TEMPLATE VERSION)

Uses Option A: inline base template + injected body HTML
(no Jinja template inheritance, so no TemplateNotFound errors)
"""

import os
from datetime import date
from flask import Flask, request, redirect, url_for, render_template_string, jsonify, flash
from flask_sqlalchemy import SQLAlchemy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'time_tracker.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret'

db = SQLAlchemy(app)

# -------------------- MODELS --------------------
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    description = db.Column(db.String(500))

    client = db.relationship('Client')

class Hour(db.Model):
    __tablename__ = 'hours'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000))

    client = db.relationship('Client')
    project = db.relationship('Project')

with app.app_context():
    db.create_all()

# -------------------- BASE TEMPLATE --------------------
base_template = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Simple Time Tracker</title>
  <style>
    body{font-family:system-ui;max-width:900px;margin:20px auto;padding:0 16px}
    nav a{margin-right:10px;text-decoration:none;padding:6px 10px;border-radius:6px}
    nav a.active{background:#ddd}
    form{margin:12px 0;padding:12px;border:1px solid #eee;border-radius:8px}
    label{display:block;margin-top:8px}
    input,select,textarea{width:100%;padding:6px}
    table{width:100%;margin-top:12px;border-collapse:collapse}
    th,td{border-bottom:1px solid #eee;padding:6px;text-align:left}
  </style>
</head>
<body>
  <h2>Simple Time Tracker</h2>
  <nav>
    <a href="/hours" class="{{ 'active' if active=='hours' else '' }}">Hours</a>
    <a href="/projects" class="{{ 'active' if active=='projects' else '' }}">Projects</a>
    <a href="/clients" class="{{ 'active' if active=='clients' else '' }}">Clients</a>
  </nav>

  {% with messages = get_flashed_messages() %}
    {% for m in messages %}<p>{{ m }}</p>{% endfor %}
  {% endwith %}

  {{ body|safe }}

  <p style="color:#777">DB: {{ db_path }}</p>
</body>
</html>
"""

# -------------------- PAGE BODIES --------------------
clients_body = """
<h3>Clients</h3>
<form method="post">
  <label>Name</label>
  <input name="name" required>
  <button>Add client</button>
</form>

<table>
{% for c in clients %}
<tr><td>{{ c.name }}</td></tr>
{% endfor %}
</table>
"""

projects_body = """
<h3>Projects</h3>
<form method="post">
  <label>Client</label>
  <select name="client_id" required>
    <option value="">-- choose --</option>
    {% for c in clients %}
      <option value="{{ c.id }}">{{ c.name }}</option>
    {% endfor %}
  </select>

  <label>Description</label>
  <input name="description">
  <button>Add project</button>
</form>

<table>
{% for p in projects %}
<tr><td>{{ p.client.name }}</td><td>{{ p.description }}</td></tr>
{% endfor %}
</table>
"""

hours_body = """
<h3>Log Hours</h3>
<form method="post">
  <label>Client</label>
  <select id="client" name="client_id" required onchange="loadProjects()">
    <option value="">-- choose --</option>
    {% for c in clients %}
      <option value="{{ c.id }}">{{ c.name }}</option>
    {% endfor %}
  </select>

  <label>Project</label>
  <select id="project" name="project_id" required></select>

  <label>Date</label>
  <input type="date" name="date" value="{{ today }}" required>

  <label>Hours</label>
  <input type="number" step="0.01" name="hours" required>

  <label>Description</label>
  <textarea name="description"></textarea>

  <button>Save</button>
</form>

<table>
{% for h in hours %}
<tr>
  <td>{{ h.date }}</td>
  <td>{{ h.client.name }}</td>
  <td>{{ h.project.description }}</td>
  <td>{{ h.hours }}</td>
</tr>
{% endfor %}
</table>

<script>
function loadProjects(){
  const clientId = document.getElementById('client').value;
  const sel = document.getElementById('project');
  sel.innerHTML = '';
  fetch('/api/projects?client_id=' + clientId)
    .then(r => r.json())
    .then(data => data.forEach(p => {
      const o = document.createElement('option');
      o.value = p.id; o.textContent = p.description || ('Project ' + p.id);
      sel.appendChild(o);
    }));
}
</script>
"""

# -------------------- ROUTES --------------------
@app.route('/')
def index():
    return redirect('/hours')

@app.route('/clients', methods=['GET','POST'])
def clients():
    if request.method == 'POST':
        db.session.add(Client(name=request.form['name']))
        db.session.commit()
        flash('Client added')
        return redirect('/clients')

    body = render_template_string(clients_body, clients=Client.query.all())
    return render_template_string(base_template, body=body, active='clients', db_path=DB_PATH)

@app.route('/projects', methods=['GET','POST'])
def projects():
    if request.method == 'POST':
        db.session.add(Project(
            client_id=request.form['client_id'],
            description=request.form.get('description')
        ))
        db.session.commit()
        flash('Project added')
        return redirect('/projects')

    body = render_template_string(
        projects_body,
        clients=Client.query.all(),
        projects=Project.query.all()
    )
    return render_template_string(base_template, body=body, active='projects', db_path=DB_PATH)

@app.route('/hours', methods=['GET','POST'])
def hours():
    if request.method == 'POST':
        db.session.add(Hour(
            client_id=request.form['client_id'],
            project_id=request.form['project_id'],
            date=date.fromisoformat(request.form['date']),
            hours=float(request.form['hours']),
            description=request.form.get('description')
        ))
        db.session.commit()
        flash('Hours logged')
        return redirect('/hours')

    body = render_template_string(
        hours_body,
        clients=Client.query.all(),
        hours=Hour.query.order_by(Hour.date.desc()).all(),
        today=date.today().isoformat()
    )
    return render_template_string(base_template, body=body, active='hours', db_path=DB_PATH)

@app.route('/api/projects')
def api_projects():
    cid = request.args.get('client_id', type=int)
    projects = Project.query.filter_by(client_id=cid).all()
    return jsonify([{'id':p.id,'description':p.description} for p in projects])

if __name__ == '__main__':
    app.run(debug=True)

