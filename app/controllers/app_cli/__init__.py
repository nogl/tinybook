from flask import Blueprint, current_app
from app import database, models

app_cli_bp = Blueprint('cli', __name__)

app_cli_bp.cli.help = 'Perform operations over application.'


@app_cli_bp.cli.command('init_db')
def init_db():
    """Create all application tables in database"""
    database.Base.metadata.create_all(bind=database.engine)


@app_cli_bp.cli.command('drop_db')
def drop_db():
    """Delete all application tables in database"""
    database.Base.metadata.drop_all(bind=database.engine)


@app_cli_bp.cli.command('seed_db')
def seed_db():
    admin = models.User()
    admin.username = 'Admin'
    admin.email = 'admin@email.com'
    database.db_session.add(admin)
    ns = models.NameSpace()
    ns.name = 'Root NS'
    ns.slug = 'root-ns'
    ns.user_id = 1
    ns2 = models.NameSpace()
    ns2.name = 'NS - 2'
    ns2.slug = 'ns-2'
    ns2.user_id = 1
    database.db_session.add(ns)
    database.db_session.add(ns2)
    database.db_session.commit()
