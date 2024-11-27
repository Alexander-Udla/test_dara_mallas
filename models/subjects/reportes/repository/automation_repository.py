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