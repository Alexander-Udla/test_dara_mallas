from ..database import base_external_dbsource as db
import pandas as pd

dbsource = db.BaseExternalDbsource()

class availabilityRepository:
    def __init__(self):
        self.database = 'banner'
    
    def get_availability_couses(self, subject):
        sql = """
            SELECT DISTINCT SCBCRSE_SUBJ_CODE
            FROM SCBCRSE
            WHERE SCBCRSE_SUBJ_CODE='%s'
            """%(subject)
        res=dbsource.query(sql=sql,option=self.database)
        return res if res else False
    
    def get_availability_curriculum(self, subject):
        sql = """
            SELECT DISTINCT SUBSTR(STVCHRT_CODE,1,4)
            FROM STVCHRT WHERE STVCHRT_CODE LIKE '%s'
            """%(subject)
        res=dbsource.query(sql=sql,option=self.database)
        return res if res else False