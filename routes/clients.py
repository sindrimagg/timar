from flask import Blueprint, render_template, request, redirect, flash
from extensions import db
from models import Client

bp = Blueprint('clients', __name__)

@bp.route('/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        db.session.add(Client(name=request.form['name']))
        db.session.commit()
        flash('Client added')
        return redirect('/clients')

    return render_template(
        'clients.html',
        clients=Client.query.all(),
        active='clients'
    )
