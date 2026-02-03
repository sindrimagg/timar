from flask import Blueprint, render_template, request, redirect, flash
from extensions import db
from models import Client, Project

bp = Blueprint('projects', __name__)

@bp.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        db.session.add(Project(
            client_id=request.form['client_id'],
            description=request.form.get('description')
        ))
        db.session.commit()
        flash('Project added')
        return redirect('/projects')

    return render_template(
        'projects.html',
        clients=Client.query.all(),
        projects=Project.query.all(),
        active='projects'
    )
