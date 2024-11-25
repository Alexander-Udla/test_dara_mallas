from ..database import base_external_dbsource as db
import pandas as pd

dbsource = db.BaseExternalDbsource('mallas_13','dara_mallas')

class METODOS_GET:
    def __init__(self) -> None:
        pass
   
    #extrae todos lo ssubjects de scadtl odoo
    def get_subjects_scadtl_odoo(self):
        sql = """
           select 
            s.code as sigla 
           ,pe.name as periodo
            from dara_mallas_subject_scadtl sca
            left join dara_mallas_subject s on sca.subject_id = s.id
            left join dara_mallas_period pe on sca.period_id = pe.id
            left join dara_mallas_coordinator co on sca.coordinador_id = co.id
            left join dara_mallas_program_code prc on sca.program_code_id = prc.id
            left join dara_mallas_weighing we on sca.weighing_id = we.id
        """
        res = dbsource.query(sql=sql,option='dara_mallas')
        return res if res else False
    #extrae todos lo ssubjects de scadtl odoo
    def get_subjects_scadtl_odoo_per_params(self,subject='',period=000000):
        sql = """
           select 
            we.code as ponderacion 
            ,co.idbanner as COORDINADOR
            ,prc.name as PROGRAMA
            from dara_mallas_subject_scadtl sca
            left join dara_mallas_subject s on sca.subject_id = s.id
            left join dara_mallas_period pe on sca.period_id = pe.id
            left join dara_mallas_coordinator co on sca.coordinador_id = co.id
            left join dara_mallas_program_code prc on sca.program_code_id = prc.id
            left join dara_mallas_weighing we on sca.weighing_id = we.id
            where s.code = '%s' and pe.name='%s'
        """%(subject,period)
        res = dbsource.query(sql=sql,option='dara_mallas',dataframe=True)
        return res 
    
    #extrae scadtl de banner por parametros
    def get_subject_scadtl_banner_per_params(self,subject='',period=000000):
        sql = """
                    SELECT SCBSUPP_CUDA_CODE AS PONDERACION
                    ,SCBSUPP_CUDC_CODE AS COORDINADOR
                    ,SCBSUPP_CUDE_CODE AS PROGRAMA
                    FROM SCBSUPP S1
                    WHERE CONCAT(SCBSUPP_SUBJ_CODE, SCBSUPP_CRSE_NUMB)  ='%s'
                    AND SCBSUPP_EFF_TERM ='%s'
            """%(subject,period)
        res = dbsource.query(sql=sql,option='banner',dataframe=True)
        return res 

