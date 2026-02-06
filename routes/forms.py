from flask import Blueprint, render_template, request, redirect, flash
from datetime import date
from sqlalchemy import exists
from extensions import db, navs
from models import Hour, Client, Project

bp = Blueprint('forms', __name__)

@bp.route('/form_hours', methods=['GET', 'POST'])
def form_hours():
    if request.method == 'POST':
        db.session.add(Hour(
            client_id=request.form['client_id'],
            project_id=request.form['project_id'],
            date=date.fromisoformat(request.form['date']),
            hours=float(request.form['hours'].replace(',','.')),
            call=request.form.get('call') == 'on',
            description=request.form.get('description')
        ))
        db.session.commit()
        flash('Tími skráður', 'info')
        return redirect('/hours')

    return render_template(
        'form.html',
        item=None,
        clients=Client.query.all(),
        projects=Project.query.all(),
        today=date.today().isoformat(),
        form_type='hours',
        navs=navs
    )
