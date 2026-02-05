# extensions.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
navs = { 'hours':'Tímar', 'projects':'Verkefni', 'clients':'Kúnnar' }
