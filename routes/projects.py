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
        item=None,
        clients=Client.query.all(),
        projects=sorted(Project.query.all(), key=lambda x: (x.client.name, x.description)),
        active='projects',
        navs=navs
    )

@bp.route('/delete/project/<int:id>', methods=['POST', 'GET'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    can_delete = Hour.query.filter_by(project_id=project.id).first() is None

    if can_delete:
        db.session.delete(project)
        db.session.commit()
        flash('Verkefni eytt', 'info')
        return redirect('/projects')
    else:
        flash('Ekki er hægt að eyða verkefni því það eru tímar skráðir á það', 'error')
        return redirect('/projects')


@bp.route('/edit/project/<int:id>', methods=['GET','POST'])
def edit_project(id):
    project = Project.query.get_or_404(id)
    all_projects = Project.query.all()
    if request.method == 'POST':
        new_cid = request.form.get('client_id')
        new_proj_desc = request.form.get('description')
        if new_cid is not None and new_proj_desc is not None:
            new_cid = int(new_cid)
            new_proj_desc = new_proj_desc.strip()
            if (new_cid, new_proj_desc) in ((proj.client.id, proj.description.strip()) for proj in all_projects if proj != project):
                new_proj_cname = Client.query.get(new_cid).name
                flash('Verkefnið ' + new_proj_desc + ' hjá ' + new_proj_cname + ' er nú þegar á skrá', 'error')
            else:
                project.client_id = new_cid
                project.description = new_proj_desc
                db.session.commit()
                flash('Verkefni uppfært', 'info')
                return redirect('/projects')
    return render_template(
        'form.html',
        form_type='projects',
        edit=True,
        item=project,
        clients=Client.query.all(),
        navs=navs,
    )
