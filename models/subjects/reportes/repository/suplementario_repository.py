class suplemetarioRepository:
    def __init__(self, env):
        self.env=env

    def get_information_banner(self, period="000000"):
        sql = """
            SELECT DISTINCT A.SCBSUPP_SUBJ_CODE, 
            A.SCBSUPP_CRSE_NUMB, 
            A.SCBSUPP_EFF_TERM,
            A.SCBSUPP_CUDA_CODE, 
            A.SCBSUPP_CUDC_CODE, 
            A.SCBSUPP_CUDE_CODE
            FROM SSBSECT
            INNER JOIN SCBSUPP A ON SSBSECT_SUBJ_CODE = A.SCBSUPP_SUBJ_CODE
            AND SSBSECT_CRSE_NUMB = A.SCBSUPP_CRSE_NUMB
            INNER JOIN (
            SELECT SCBSUPP_SUBJ_CODE, SCBSUPP_CRSE_NUMB, MAX(SCBSUPP_EFF_TERM) TERM
            FROM SCBSUPP
            GROUP BY SCBSUPP_SUBJ_CODE, SCBSUPP_CRSE_NUMB
            ) B ON A.SCBSUPP_SUBJ_CODE = B.SCBSUPP_SUBJ_CODE
            AND A.SCBSUPP_CRSE_NUMB = B.SCBSUPP_CRSE_NUMB
            WHERE SSBSECT_TERM_CODE=:period
            """
        dbsource=self.env['base.external.dbsource'].search([('enabled','=',True)])
        if not dbsource:
            return False
        res = dbsource.execute(sql, {'period': period})
        return res if res else False