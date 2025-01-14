from ..database import base_external_dbsource as db
import pandas as pd

dbsource = db.BaseExternalDbsource()

class acronymRepository:
    def __init__(self):
        self.database = 'banner'
        
        
    def get_acronym_per_comparison(self, acronym1 , acronym2):
        sql = """
            SELECT aux_gorsdav.*
            FROM SCBCRSE
            INNER JOIN 
            (SELECT SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB SUBJ, MAX(SCBCRSE_EFF_TERM) TERM
            FROM SCBCRSE
            GROUP BY SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB
            ) AX_CRSE ON SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB = AX_CRSE.SUBJ
            AND SCBCRSE_EFF_TERM = AX_CRSE.TERM
            INNER JOIN (
            SELECT SMRACAA_RULE REGLA
            FROM SMRACAA 
            INNER JOIN (
            SELECT SMRACAA_AREA AREA, MAX(SMRACAA_TERM_CODE_EFF) TERM
            FROM SMRACAA
            GROUP BY SMRACAA_AREA
            ) REGLA ON REGLA.AREA=SMRACAA_AREA
            AND REGLA.TERM=SMRACAA_TERM_CODE_EFF
            ) AX_REGLA ON AX_REGLA.REGLA=SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB
            INNER JOIN (
            SELECT * FROM
            (
            SELECT SUBSTR(GORSDAV_PK_PARENTTAB,1,4)||SUBSTR(GORSDAV_PK_PARENTTAB,6,4) SUBJ,SUBSTR(GORSDAV_PK_PARENTTAB,11,6) TERM,
            GORSDAV_ATTR_NAME ATTR, GORSDAV_VALUE VALUE
            FROM GORSDAV 
            WHERE GORSDAV_TABLE_NAME='SCBCRSE'
            )
            PIVOT (
            MAX(SYS.ANYDATA.accessVarchar2(VALUE))
            FOR ATTR IN (
            'HORAS_DOCENCIA',
            'HORAS_DOCENCIA_PRESENCIAL_H',
            'HORAS_DOCENCIA_VIRTUAL_H',
            'HORAS_DOCENCIA_O',
            'HORAS_LABORATORIO_DOCENCIA',
            'HORAS_LABORATORIO_DOCENCIA_H',
            'HORAS_EXTERNADO_DOCENCIA',
            'HORAS_EXTERNADO_DOCENCIA_H',
            'HORAS_APLICACION',
            'HORAS_APLICACION_H',
            'HORAS_APLICACION_O',
            'HORAS_APLICACION_LABORATORIO',
            'HORAS_APLICACION_LAB_H',
            'HORAS_APLICACION_LAB_O',
            'HORAS_PRACT_PREPROFESIONALES',
            'HORAS_PRACT_PREPROF_H',
            'HORAS_PRACT_PREPROF_O',
            'HORAS_SERVICIO_COMUNIDAD',
            'HORAS_SERVICIO_COMUNIDAD_H',
            'HORAS_SERVICIO_COMUNIDAD_O',
            'TOTAL_HORAS_AUTONOMAS',
            'TOTAL_HORAS_AUTONOMAS_H',
            'TOTAL_HORAS_AUTONOMAS_O',
            'HORAS_TITULACION',
            'HORAS_TITULACION_H',
            'HORAS_TITULACION_O',
            'SESIONES_DOCENCIA',
            'SESIONES_LABORATORIO',
            'SESIONES_EXTERNADO',
            'SESIONES_O',
            'SEMANAS_EXTERNADO',
            'SEMANAS_LABORATORIO',
            'HORAS_ADICIONALES_SILABO')
            )) AUX_GORSDAV ON AUX_GORSDAV.SUBJ=SCBCRSE_SUBJ_CODE||SCBCRSE_CRSE_NUMB
            AND AUX_GORSDAV.TERM=SCBCRSE_EFF_TERM
            AND AUX_GORSDAV.SUBJ IN ('%s', '%s')
            """%(acronym1,acronym2)        
        res = dbsource.query(sql=sql,option=self.database)
        return res if res else False
        