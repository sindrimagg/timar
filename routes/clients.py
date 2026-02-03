from flask import Blueprint, render_template, request, redirect, flash
from sqlalchemy import exists
from extensions import db
from models import Client

bp = Blueprint('clients', __name__)

@bp.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        client = request.form['name']
        client_exists = db.session.query(exists().where(Client.name == client)).scalar()
        print('Client exists', client, client_exists)
        if client_exists:
            flash('Þessi kúnni er nú þegar á skrá', 'error')
        else:
            db.session.add(Client(name=client))
            db.session.commit()
            flash('Kúnnanum var bætt við', 'info')
            return redirect('/clients')

    return render_template(
        'clients.html',
        clients=Client.query.all(),
        active='clients'
    )
