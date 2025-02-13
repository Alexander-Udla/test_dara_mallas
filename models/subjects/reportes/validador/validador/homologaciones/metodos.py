from database import base_external_dbsource as db
import pandas as pd

dbsource = db.BaseExternalDbsource('mallas_13','dara_mallas')

class Validator:
    def __init__(self, env) -> None:
        self.database = 'dara_mallas_dev'
        self.databasebanner = env
    
    def get_homologations_for_period(self,period='000000'):
        sql = """
            select a2.code as "AREA",s2.code as "REGLA",max(pe2.name) AS "PERIODO" from  dara_mallas_subject_rule sr 
            left join dara_mallas_area a2 on sr.area_id = a2.id
            left join dara_mallas_period pe2 on sr.period_id = pe2.id
            left join dara_mallas_subject s2 on sr.subject_id = s2.id
            where (a2.code ,s2.code)in(
            select a.code,s.code from dara_mallas_area_homologation ah 
            left join dara_mallas_period pe on ah.period_id = pe.id
            left join dara_mallas_area a on ah.area_id = a.id
            left join dara_mallas_subject_inherit_area sia on ah.id = sia.area_homologation_id
            left join dara_mallas_subject_inherit si on sia.subject_inherit_id = si.id
            left join dara_mallas_subject s on si.subject_id = s.id
            where pe.name = '%s'
            --and a.code = '014-S01'
            )
            and pe2.name <= '%s'
            group by a2.code,s2.code
            limit 10
        """%(period,period)
        print("Database parametro ", self.database)
        res = dbsource.query(sql=sql,option=self.database)
        return res if res else False

    def get_homologations_for_subject_period_area(self,subject_code="",period="",area="",period_val="000000"):
        if period == 0:
            period = '000000'
        sql = """
            select '%s' as "PERIODO"
                ,a.code as "AREA" 
                ,s.code as "REGLA"
                -- ,h.condition as condition
                ,g.name as "CONECTOR"
                ,sh.code as "SIGLA" 
                ,case when h.test='0' then null else h.test end as "PRUEBA"
                ,case when h.min_score='0' then null else h.min_score end as "TEST_PUNTAJE_MINIMO"
                ,case when h.max_score='0' then null else h.max_score end as "TEST_PUNTAJE_MAXIMO"
                ,(select name from dara_mallas_rule_score where id =h.rule_min_score_id) as "REGLA_PUNTAJE_MINIMO"
                ,sa.name as "REGLA_ATRIBUTO"
                from dara_mallas_subject_rule sr
                left join dara_mallas_area a on sr.area_id = a.id
                left join dara_mallas_homologation h on sr.id = h.subject_rule_id
                left join dara_mallas_group_rule g on h.group_id = g.id
                left join dara_mallas_subject s on sr.subject_id = s.id
                left join dara_mallas_subject sh on h.homologation_subject_id = sh.id
                left join dara_mallas_period pe on sr.period_id = pe.id
                left join dara_mallas_subject_attributes sa on h.subject_attributes_id = sa.id
                where 
				s.code = '%s'
                and pe.name = '%s'
                and a.code = '%s'
            order by 2,4;
        """%(period_val,subject_code,period,area)
        res = dbsource.query(sql=sql,option=self.database)
        return res if res else False

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
        """%(area,subject_code,period)
        #res = dbsource.query(sql=sql,option='banner')
        res = dbsource.query(sql=sql,option=self.databasebanner)
        return res if res else False


    
