from ..database import base_external_dbsource as db
import pandas as pd

dbsource = db.BaseExternalDbsource()

class availabilityRepository:
    def __init__(self):
        self.database = 'banner'
    
    def get_availability_couses(self, subject):
        pass
    
    
    def get_availability_curriculum(self, subject):
        pass