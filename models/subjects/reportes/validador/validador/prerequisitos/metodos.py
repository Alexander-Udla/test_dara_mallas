from database import base_external_dbsource as db
import pandas as pd

dbsource = db.BaseExternalDbsource('mallas_13','dara_mallas')

class Validator:
    def __init__(self, env) -> None:
        self.database_odoo = "dara_mallas_dev"
        self.database_banner = env
        

    def delete_detail(self,id):
        sql = """delete from dara_mallas_prerequisite where prerequisite_line_id = %s ;\n"""%(id)
        return sql

    #extra el detalle de los prerequisitos
    def get_prerequisito_odoo_detail(self,subject_code=None,period=None):
        sql = """
            select case when pr.conector = 'Y' then 'A' else pr.conector end as conector,
            pr.lparen,pr.test_code,pr.test_score,spre.code as prerequisite_subject_code,rs.name as rule_score,pr.rparen,pr.seq
            from dara_mallas_prerequisite pr
            left join dara_mallas_prerequisite_line prl on pr.prerequisite_line_id = prl.id
            left join dara_mallas_subject s on prl.subject_id = s.id
            left join dara_mallas_period pe on prl.period_id = pe.id
            left join dara_mallas_subject spre on pr.prerequisite_subject_id = spre.id
            left join dara_mallas_rule_score rs on pr.score_id = rs.id
            where s.code = '%s' and pe.name = '%s' 
            order by 8
            limit 10
        """%(subject_code,period)
        res = dbsource.query(sql=sql,option=self.database_odoo,dataframe=True)
        return res
    
    def get_subject_prerequisito_odoo_per_period(self,period=None):
        # trae todas las siglas de prerequisito por periodo
        sql = """
            select s.code as subject_code ,pe.name as period from dara_mallas_prerequisite_line pl
            left join dara_mallas_subject s on pl.subject_id = s.id
            left join dara_mallas_period pe on pl.period_id = pe.id
            where pe.name = '%s'
            order by 1
            limit 10
        """%(period)
        res = dbsource.query(sql=sql,option=self.database_odoo,dataframe=True)
        return res

    #extrae el id de la cabecera
    def get_id_prerequisito_odoo_head(self,periodo=None,subject_code=None):
        sql = """
            select distinct prl.id from dara_mallas_prerequisite_line prl 
            left join dara_mallas_subject s on prl.subject_id = s.id          
            left join dara_mallas_period pe on prl.period_id = pe.id    
            where s.code = '%s' and pe.name = '%s'
            limit 10
        """%(subject_code,periodo)
        res = dbsource.query(sql=sql,option=self.database_odoo)
        return res if res else False

    def get_prerequisitos_banner_detail(self,subject_code,period):
        sql = """  
                SELECT  SCRRTST_SEQNO as seq
                ,SCRRTST_SUBJ_CODE||SCRRTST_CRSE_NUMB as subject_code
                ,COALESCE(SCRRTST_CONNECTOR,'') as conector
                ,COALESCE(SCRRTST_LPAREN,'') as lparen
                ,COALESCE(SCRRTST_TESC_CODE,'') as test_code
                ,COALESCE( SCRRTST_TEST_SCORE,'') as test_score
                ,COALESCE(SCRRTST_SUBJ_CODE_PREQ||SCRRTST_CRSE_NUMB_PREQ ,'')as prerequisite_subject_code
                ,COALESCE(SCRRTST_MIN_GRDE,'') as rule_score
                ,COALESCE(SCRRTST_RPAREN,'') as rparen
                ,SCRRTST_TERM_CODE_EFF as period 
                FROM SCRRTST
                where SCRRTST_SUBJ_CODE||SCRRTST_CRSE_NUMB =:1 
                and SCRRTST_TERM_CODE_EFF =:2
                ORDER BY 2,1
                limit 10
                """
        
        result = dbsource.query(sql=sql,option=self.database_banner,parq=[subject_code,period],dataframe=True)
        return result

    def get_subject_prerequisites(subject_code):
        sql = """  
                select     s.code as subject_code
                    ,s.id as subject_id
                    ,p.seq as seq
                    ,case when p.conector = 'Y' then 'A' else p.conector end as conector
                    ,p.lparen as lparen
                    ,coalesce(p.test_code,'') as test_code
                    ,p.test_score as test_score
                    ,coalesce(ps.code,'') as prerequisite_subject_code
                    ,ps.id as prerequisite_subject_id
                    ,coalesce(g.name,'') as grade
                    ,g.id as grade_id
                    ,coalesce(sc.name,'') as score
                    ,sc.id as score_id
                    ,rparen
                from udla_mallas_prerequisite p 
                left join udla_mallas_subject s on p.subject_id = s.id
                left join udla_mallas_subject ps on p.prerequisite_subject_id = ps.id
                left join udla_mallas_grade g on p.grade_id = g.id
                left join udla_mallas_rule_score sc on p.score_id = sc.id
                where s.code = %s
                order by s.code, p.seq
                limit 10
        """
        
        result = dbsource.get_dataframe_from_postgres(sql,[subject_code])

        return result
    
    def get_odoo_prerequisites_in_line (subject_code):
        df_result = get_subject_prerequisites(subject_code)
        odoo_prereq=[]
        for index, row in df_result.iterrows():
            if row['conector']:
                odoo_prereq.append(row['conector'])
            if row['lparen']:
                odoo_prereq.append(row['lparen'])
            if row['test_code']:
                odoo_prereq.append(row['test_code'])
            if row['test_score']:
                odoo_prereq.append(int(row['test_score']))
            if row['prerequisite_subject_code']:
                odoo_prereq.append(row['prerequisite_subject_code'])
            if row['rparen']:
                odoo_prereq.append(row['rparen'])
        return odoo_prereq
    
    def get_homologations_for_subject_period_area_banner(self,subject_code="",period="",area=""):
        if period == 0:
            period = '000000'
        sql = """
            select 
                    SMRARUL_TERM_CODE_EFF as PERIODO
                    ,smrarul_area AS AREA
                    ,smrarul_key_rule AS REGLA
                    ,smrarul_set||'-'||smrarul_subset AS CONECTOR
                    ,SMRARUL_SUBJ_CODE||SMRARUL_CRSE_NUMB_LOW AS SIGLA
                    ,SMRARUL_TESC_CODE AS PRUEBA
                    ,SMRARUL_MIN_VALUE AS "TEST_PUNTAJE_MINIMO"
                    ,SMRARUL_MAX_VALUE AS "TEST_PUNTAJE_MAXIMO"
                    ,SMRARUL_GRDE_CODE_MIN AS "REGLA_PUNTAJE_MINIMO"
                    ,SMRARUL_ATTR_CODE AS "REGLA_ATRIBUTO"
                from smrarul
                    where
                    smrarul_area = '%s'
                    and smrarul_key_rule = '%s'
                    and SMRARUL_TERM_CODE_EFF='%s'
                    order by 2,4
                    limit 10
        """%(area,subject_code,period)
        res = dbsource.query(sql=sql,option='banner')
        return res if res else False


    
