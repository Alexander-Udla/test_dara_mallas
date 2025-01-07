from ..database import base_external_dbsource as db

dbsource = db.BaseExternalDbsource()

class automationRepository:
    def __init__(self):
        self.database = 'banner'
        
    def get_program_postrado(self, dateToday):
        sql = """
            SELECT DISTINCT SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE) CODIGO_PROGRAMA,
            SMRPRLE_PROGRAM_DESC PROGRAMA,
            GORSDAV_PK_PARENTTAB COHORTE_PROGRAMA
            FROM GORSDAV
            INNER JOIN SMRPRLE ON SMRPRLE_PROGRAM=SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE)
            WHERE GORSDAV_TABLE_NAME='STVCHRT'
            AND GORSDAV_ATTR_NAME='CODIGO_PROGRAMA'
            AND SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE) LIKE 'UDLA%%'
            AND GORSDAV_PK_PARENTTAB IN (
            SELECT GORSDAV_PK_PARENTTAB
            FROM GORSDAV
            WHERE GORSDAV_TABLE_NAME='STVCHRT'
            AND GORSDAV_ATTR_NAME='FECHA_INICIO'
            AND TO_CHAR(SYS.ANYDATA.accessDate(GORSDAV_VALUE), 'DD-MON-YYYY')='%s')
            """%(dateToday)
        res=dbsource.query(sql=sql,option=self.database)
        return res if res else False
    
    #cantidad de alumnos
    def get_number_student(self):
        sql= """
            SELECT DISTINCT 
                SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE) AS CODIGO_PROGRAMA,
                SMRPRLE_PROGRAM_DESC AS PROGRAMA,
                GORSDAV_PK_PARENTTAB AS COHORTE_PROGRAMA,
                (SELECT COUNT(DISTINCT SOVLCUR_PIDM)
                FROM SOVLCUR
                INNER JOIN SGRSTSP
                ON SGRSTSP_PIDM = SOVLCUR_PIDM
                AND SGRSTSP_TERM_CODE_EFF = SOVLCUR_TERM_CODE
                AND SGRSTSP_KEY_SEQNO = SOVLCUR_KEY_SEQNO
                AND SGRSTSP_STSP_CODE = 'AS' -- PLAN DE ESTUDIOS ACTIVO
                INNER JOIN SGRCHRT 
                ON SOVLCUR_PIDM = SGRCHRT_PIDM
                AND SGRCHRT_CHRT_CODE = GORSDAV_PK_PARENTTAB -- Utiliza el COHORTE_PROGRAMA aquí
                WHERE SOVLCUR_CURRENT_IND = 'Y' -- ACTUAL
                AND SOVLCUR_ACTIVE_IND = 'Y' -- ACTIVO
                AND SOVLCUR_LMOD_CODE = 'LEARNER'
                AND SOVLCUR_STYP_CODE IN ('N','T','X','C','R','S','U')
                ) AS NUMERO_ESTUDIANTES -- Nueva columna con el conteo
                FROM GORSDAV
                INNER JOIN SMRPRLE 
                ON SMRPRLE_PROGRAM = SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE)
                WHERE GORSDAV_TABLE_NAME = 'STVCHRT'
                AND GORSDAV_ATTR_NAME = 'CODIGO_PROGRAMA'
                AND SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE) LIKE 'UDLA%'
                AND GORSDAV_PK_PARENTTAB IN (
                SELECT GORSDAV_PK_PARENTTAB
                FROM GORSDAV
                WHERE GORSDAV_TABLE_NAME = 'STVCHRT'
                AND GORSDAV_ATTR_NAME = 'FECHA_INICIO'
                AND TO_CHAR(SYS.ANYDATA.accessDate(GORSDAV_VALUE), 'DD-MON-YYYY') = '25-NOV-2024')
            """
        res=dbsource.query(sql=sql,option=self.database)
        return res if res else False
    
    def get_number_cohorte(self, codigo):
        sql="""
            SELECT GORSDAV_PK_PARENTTAB,
            ROW_NUMBER() OVER (ORDER BY TO_DATE(SUBSTR(REGEXP_REPLACE(GORSDAV_PK_PARENTTAB, '[^0-9]', ''), 3, 4) || '-' || SUBSTR(REGEXP_REPLACE(GORSDAV_PK_PARENTTAB, '[^0-9]', ''), 1, 2), 'YYYY-MM') ) AS POSICION
            FROM GORSDAV 
            WHERE GORSDAV_TABLE_NAME = 'STVCHRT' 
            AND SYS.ANYDATA.accessVarchar2(GORSDAV_VALUE) = '%s'        
            """%(codigo)
        res=dbsource.query(sql=sql,option=self.database)
        return res if res else False