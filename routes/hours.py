from flask import Blueprint, render_template, request, redirect, jsonify, flash, url_for, send_file
from datetime import date, timedelta
from extensions import db, navs
from models import Project, Hour, Client
import csv

bp = Blueprint('hours', __name__)

def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Unsupported date format: {date_str}")

@bp.route('/hours', methods=['GET', 'POST'])
def hours():
    clients = Client.query.all()

    client_id = request.args.get('client_id', type=int)
    project_id = request.args.get('project_id', type=int)
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = [client_id, project_id, start_date, end_date]

    q = Hour.query
    if not any(query):
        q = q.filter(Hour.date >= (date.today() - timedelta(weeks=1)))
    else:
        if client_id:
            q = q.filter(Hour.client_id == client_id)

        if project_id:
            q = q.filter(Hour.project_id == project_id)

        if start_date:
            q = q.filter(Hour.date >= start_date)

        if end_date:
            q = q.filter(Hour.date <= end_date)

    with open("files/query.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        header = ['Dagsetning', 'Kúnni', 'Verkefni', 'Tímar', 'Lýsing']
        writer.writerow(header)
        for data in q.order_by(Hour.date.asc()):
            writer.writerow([str(data.date), data.client.name, data.project.description, str(data.hours), data.description])


    return render_template(
        'hours.html',
        hours=q.order_by(Hour.date.desc()).all(),
        clients=clients,
        query=query,
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

@bp.route('/download')
def download():
    return send_file("files/query.csv", as_attachment=True, download_name="timar.csv")
