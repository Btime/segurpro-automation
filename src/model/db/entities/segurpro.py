from sqlalchemy import Column, String, Integer, Boolean, DateTime
from src.model.db.configs.base import Base

class Segurpro(Base):
    
    __tablename__ = "tb_segurpro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_activity = Column(Integer)
    rov = Column(Integer)
    id_children = Column(Integer)
    status = Column(String)
    site_name = Column(String)
    system = Column(String)
    description = Column(String)
    triage = Column(Boolean)
    created_at = Column(DateTime)

    def __repr__(self):
        return f"Segurpro [ROV='{self.rov}', Status='{self.status}', Location='{self.site_name}', System='{self.system}, Description='{self.description}', Triage='{self.triage}']"
