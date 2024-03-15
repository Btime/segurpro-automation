from sqlalchemy import Column, String, Integer, Boolean, DateTime
from src.model.db.configs.base import Base


class Segurpro(Base):

    __tablename__ = "tb_segurpro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_activity = Column(Integer)
    rov = Column(Integer)
    id_children = Column(Integer)
    status_mse = Column(String)
    site_name = Column(String)
    system = Column(String)
    opening_reason = Column(String)
    status_btime = Column(String)
    triage = Column(Boolean)
    created_at = Column(DateTime)

    def __repr__(self):
        return f"Segurpro [ROV='{self.rov}', Status_MSE='{self.status_mse}', Location='{self.site_name}', System='{self.system}, Opening_Reason='{self.opening_reason}', Status_Btime='{self.status_btime}', Triage='{self.triage}']"
