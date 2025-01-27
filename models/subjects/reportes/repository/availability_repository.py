class availabilityRepository:
    def __init__(self, env):
        self.env = env 
    
    def get_availability_couses(self, subject):
        sql = """
            SELECT DISTINCT SCBCRSE_SUBJ_CODE
            FROM SCBCRSE
            WHERE SCBCRSE_SUBJ_CODE=:subject
            """
        dbsource=self.env['base.external.dbsource'].search([('enabled','=',True)])
        if not dbsource:
            return False
        res = dbsource.execute(sql, {'subject': subject})
        return res if res else False
    
    def get_availability_curriculum(self, subject):
        sql = """
            SELECT DISTINCT SUBSTR(STVCHRT_CODE,1,4)
            FROM STVCHRT WHERE STVCHRT_CODE LIKE :subject
            """
        dbsource=self.env['base.external.dbsource'].search([('enabled','=',True)])
        if not dbsource:
            return False
        res = dbsource.execute(sql, {'subject': subject})
        return res if res else False