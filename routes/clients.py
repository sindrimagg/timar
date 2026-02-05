from flask import Blueprint, render_template, request, redirect, flash
from sqlalchemy import exists
from extensions import db, navs
from models import Client, Project, Hour

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
        item=None,
        clients=Client.query.all(),
        active='clients',
        navs=navs
    )

@bp.route('/delete/client/<int:id>', methods=['POST', 'GET'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    can_delete = Hour.query.filter_by(client_id=client.id).first() is None and Project.query.filter_by(client_id=client.id).first() is None

    if can_delete:
        db.session.delete(client)
        db.session.commit()
        flash('Kúnna eytt', 'info')
        return redirect('/clients')
    else:
        flash('Ekki er hægt að eyða kúnna því það eru tímar eða verkefni skráðir á hann', 'error')
        return redirect('/clients')


@bp.route('/edit/client/<int:id>', methods=['GET','POST'])
def edit_client(id):
    client = Client.query.get_or_404(id)
    clients = Client.query.all()
    if request.method == 'POST':
        new_name = request.form.get('name')
        if new_name in (clnt.name for clnt in clients if clnt != client):
            flash(new_name + ' er nú þegar á skrá', 'error')
        else:
            client.name=new_name
            db.session.commit()
            flash('Kúnni uppfærður', 'info')
            return redirect('/clients')
    return render_template(
        'form.html',
        form_type='clients',
        edit=True,
        item=client,
        clients=clients,
        navs=navs,
    )
