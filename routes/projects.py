from flask import Blueprint, render_template, request, redirect, flash
from sqlalchemy import exists
from extensions import db
from models import Client, Project

bp = Blueprint('projects', __name__)

@bp.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        client_id = request.form['client_id']
        description = request.form.get('description')
        project = Project(
            client_id=client_id,
            description=description,
        )
        project_exists = db.session.query(exists().where((Project.client_id == client_id) & (Project.description == description))).scalar()
        if project_exists:
            flash('Þetta verkefni er nú þegar til', 'error')
        else:
            db.session.add(project)
            db.session.commit()
            flash('Verkefninu var bætt við', 'info')
            return redirect('/projects')

    return render_template(
        'projects.html',
        clients=Client.query.all(),
        projects=Project.query.all(),
        active='projects'
    )
