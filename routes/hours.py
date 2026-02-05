from flask import Blueprint, render_template, request, redirect, jsonify, flash, url_for
from datetime import date
from extensions import db, navs
from models import Project, Hour, Client

bp = Blueprint('hours', __name__)

@bp.route('/hours', methods=['GET', 'POST'])
def hours():
    return render_template(
        'hours.html',
        hours=Hour.query.order_by(Hour.date.desc()).all(),
        active='hours',
        navs=navs
    )

@bp.route('/api/projects')
def api_projects():
    cid = request.args.get('client_id', type=int)
    projects = Project.query.filter_by(client_id=cid).all()
    return jsonify([{'id': p.id, 'description': p.description} for p in projects])

@bp.route('/delete/hours/<int:id>', methods=['POST', 'GET'])
def delete_item(id):
    item = Hour.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Færslu eytt', 'info')
    return redirect(url_for('hours.hours'))

@bp.route('/edit/hours/<int:id>', methods=['GET','POST'])
def edit(id):
    item = Hour.query.get_or_404(id)
    if request.method == 'POST':
        item.client_id=request.form['client_id']
        item.project_id=request.form['project_id']
        item.date=date.fromisoformat(request.form['date'])
        item.hours=float(request.form['hours'].replace(',','.'))
        item.description=request.form.get('description')
        db.session.commit()
        flash('Færsla uppfærð', 'info')
        return redirect('/hours')
    return render_template(
        'form.html',
        form_type='hours',
        edit=True,
        item=item,
        clients=Client.query.all(),
        projects=sorted(Project.query.all(), key=lambda x: (x.client.name, x.description)),
        navs=navs,
    )
