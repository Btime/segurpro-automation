from datetime import datetime
from src.model.db.configs.connection import DBConnectionHandler
from src.model.db.entities.segurpro import Segurpro
from sqlalchemy import text, update
from src.model.db.configs.base import Base

date = datetime.now()

class SegurproRepository:
    def __init__(self) -> None:
        self.create_table()        
    
    def create_table(self):
        with DBConnectionHandler() as db:
            query = text(
                """
                    CREATE TABLE IF NOT EXISTS tb_segurpro
                    (id INTEGER PRIMARY KEY, ID_ACTIVITY INTEGER, ROV INTEGER, STATUS TEXT, SITE_NAME TEXT, SYSTEM TEXT, DESCRIPTION TEXT, TRIAGE INTEGER, CREATED_AT DATETIME)
                """
            )
            db.session.execute(query)
            db.session.commit()

    def filter_by_rov(self, rov):
        with DBConnectionHandler() as db:
            data = db.session.query(Segurpro).filter(Segurpro.rov == rov).first()
            return data

    def select(self):
        with DBConnectionHandler() as db:
            data = db.session.query(Segurpro).all()
            return data

    def insert(self, id_activity, rov, status, site_name, system, description, triage):
        with DBConnectionHandler() as db:
            data_insert = Segurpro(
                id_activity = id_activity,
                rov = rov,
                status = status,
                site_name = site_name,
                system = system,
                description = description,
                triage = triage,
                created_at = date
            )
            db.session.add(data_insert)
            db.session.commit()
    
    def update(self, column, id, value):
        with DBConnectionHandler() as db:
            query = update(Segurpro).where(Segurpro.id_activity == id).values({column: value})
            db.session.execute(query)
            db.session.commit()