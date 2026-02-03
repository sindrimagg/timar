from flask import Blueprint, render_template, request, redirect, jsonify, flash
from datetime import date
from extensions import db
from models import Client, Project, Hour

bp = Blueprint('hours', __name__)

@bp.route('/hours', methods=['GET', 'POST'])
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

    return render_template(
        'hours.html',
        clients=Client.query.all(),
        hours=Hour.query.order_by(Hour.date.desc()).all(),
        today=date.today().isoformat(),
        active='hours'
    )

@bp.route('/api/projects')
def api_projects():
    cid = request.args.get('client_id', type=int)
    projects = Project.query.filter_by(client_id=cid).all()
    return jsonify([{'id': p.id, 'description': p.description} for p in projects])
