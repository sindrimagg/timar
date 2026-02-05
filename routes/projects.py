from flask import Blueprint, render_template, request, redirect, flash, url_for
from sqlalchemy import exists
from extensions import db, navs
from models import Client, Project, Hour

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
        projects=sorted(Project.query.all(), key=lambda x: (x.client.name, x.description)),
        active='projects',
        navs=navs
    )

@bp.route('/delete/project/<int:id>', methods=['POST', 'GET'])
def delete_item(id):
    item = Project.query.get_or_404(id)
    can_delete = Hour.query.filter_by(project_id=item.id).first() is None

    if can_delete:
        db.session.delete(item)
        db.session.commit()
        flash('Verkefni eytt', 'info')
        return redirect('/projects')
    else:
        flash('Ekki er hægt að eyða verkefni því það eru tímar skráðir á það', 'error')
        return redirect('/projects')
