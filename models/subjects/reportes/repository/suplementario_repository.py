class suplemetarioRepository:
    def __init__(self, env):
        self.env=env

    def get_information_banner(self, period="000000"):
        sql = """
            SELECT DISTINCT A.SCBSUPP_SUBJ_CODE ||
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
            AND A.SCBSUPP_EFF_TERM =  B.TERM
            WHERE SSBSECT_TERM_CODE=:period
            FETCH FIRST 20 ROWS ONLY
            """
        dbsource=self.env['base.external.dbsource'].search([('enabled','=',True)])
        if not dbsource:
            return False
        res = dbsource.execute(sql, {'period': period})
        return res if res else False
    

    def get_information_odoo(self, code="000000"):
        sql = """
            SELECT DISTINCT 
                dms.code, 
                MAX(dmp.name) AS periodo, 
                MAX(SPLIT_PART(dmw.name, '(', 1)) AS ponderacion, 
                MAX(dmc.idbanner) AS coordinador, 
                MAX(dmpc.name) AS programa
            FROM dara_mallas_subject dms
            JOIN dara_mallas_subject_scadtl dmssc ON dms.id = dmssc.subject_id
            JOIN dara_mallas_weighing dmw ON dmw.id = dmssc.weighing_id
            JOIN dara_mallas_coordinator dmc ON dmc.id = dmssc.coordinador_id
            JOIN dara_mallas_program_code dmpc ON dmpc.id = dmssc.program_code_id
            JOIN dara_mallas_period dmp ON dmp.id = dmssc.period_id
            WHERE dms.code = %s
            GROUP BY dms.code
            """
        self.env.cr.execute(sql, (code,))
        result = self.env.cr.fetchall()  # Lista de tuplas con los datos
        
        return result if result else False