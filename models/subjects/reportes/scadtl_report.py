from odoo import fields, models,api
import openpyxl
from openpyxl.styles import PatternFill
from io import BytesIO
import base64
from datetime import date, datetime
import cx_Oracle
class scadtl_report(models.Model):
    _name="dara_mallas.scadtl_report"
    file=fields.Binary("Reporte")
    file_name=fields.Char("Reporte de diferencias con banner")
    subject = fields.Many2one("dara_mallas.subject")
    period = fields.Many2one("dara_mallas.period")

    def get_odoo_subject_details(self):
        scadtl_records = self.env['dara_mallas.subject_scadtl'].search([
            #('subject_id', '=', self.subject.id),
            ('period_id', '=', self.period.id)
        ])
        return scadtl_records

    def get_banner_subject_details(self):
        db_user = "INT_MALLAS"
        db_pass = "8jAbdj4TWRX8@3q*"
        db_server = "snora06.udla-ec.int"
        db_port = "1521"
        db_sid = "PRODSTBY"

        # Configurar la cadena de conexión
        dsn_tns = cx_Oracle.makedsn(db_server, db_port, service_name=db_sid)

        # Establecer la conexión
        conn = cx_Oracle.connect(user=db_user, password=db_pass, dsn=dsn_tns)

        # Crear un cursor para ejecutar la consulta
        cur = conn.cursor()

        # Definir la consulta SQL con los parámetros
        sql = '''
        SELECT DISTINCT SCBSUPP_SUBJ_CODE||SCBSUPP_CRSE_NUMB subject, SCBSUPP_CUDA_CODE weighing, SCBSUPP_CUDC_CODE coordinator, SCBSUPP_CUDE_CODE program
        FROM SCBSUPP
        INNER JOIN (
            SELECT SCBSUPP_SUBJ_CODE a, SCBSUPP_CRSE_NUMB b, max(SCBSUPP_EFF_TERM) c
            FROM SCBSUPP
            GROUP BY SCBSUPP_SUBJ_CODE, SCBSUPP_CRSE_NUMB
        ) AUX ON SCBSUPP_SUBJ_CODE = AUX.a
        AND SCBSUPP_CRSE_NUMB = AUX.b
        --AND SCBSUPP_SUBJ_CODE||SCBSUPP_CRSE_NUMB = :subj_code
        AND SCBSUPP_EFF_TERM = AUX.c
        INNER JOIN SSBSECT ON SSBSECT_SUBJ_CODE||SSBSECT_CRSE_NUMB=SCBSUPP_SUBJ_CODE||SCBSUPP_CRSE_NUMB
        AND SSBSECT_TERM_CODE = :term_code
        '''

        # Ejecutar la consulta con los parámetros
        #cur.execute(sql, subj_code=self.subject.code, term_code=self.period.name)
        
        cur.execute(sql, term_code=self.period.name)

        # Obtener los resultados
        banner = cur.fetchall()

        # Cerrar la conexión y el cursor
        cur.close()
        conn.close()

        return banner

    def generate_report(self):
        banner_details = self.get_banner_subject_details()
        odoo_details = self.get_odoo_subject_details()

        banner_dict = {
            f"{record[0]}": (record[1], record[2], record[3]) for record in banner_details
        }

        file_data = []

        for odoo_record in odoo_details:
            period = self.period.name
            subject = odoo_record.subject_id.code
            coordinator_odoo = odoo_record.coordinador_id.idbanner
            program_odoo = odoo_record.program_code_id.name
            weighing_odoo = odoo_record.weighing_id.code

            diff_coordinator = ""
            diff_program = ""
            diff_weighing = ""

            banner_record = banner_dict.get(subject)

            if banner_record:
                weighing_banner, coordinator_banner, program_banner = banner_record
                
                if coordinator_odoo != coordinator_banner:
                    diff_coordinator = "modified"
                
                if program_odoo != program_banner:
                    diff_program = "modified"
                
                if weighing_odoo != weighing_banner:
                    diff_weighing = "modified"
                
                del banner_dict[subject]
            else:
                diff_coordinator = "not found banner"
                diff_program = "not found banner"
                diff_weighing = "not found banner"

            file_data.append([
                period, subject, coordinator_odoo, program_odoo, weighing_odoo,
                diff_coordinator, diff_program, diff_weighing
            ])

            file_data.append([
                period, subject,  coordinator_banner, program_banner,weighing_banner
            ])

        for subject, banner_record in banner_dict.items():
            period = self.period.name
            coordinator_banner = banner_record[0]
            weighing_banner = banner_record[1]
            program_banner = banner_record[2]

            file_data.append([
                period, subject, coordinator_banner, program_banner, weighing_banner,
                "not found odoo", "not found odoo", "not found odoo"
            ])

        self.save_to_excel(file_data)

    def save_to_excel(self, file_data):
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title ="SCADTL odoo banner"

        fill_modified = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        fill_added = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
        fill_removed = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

        header = ["PERIODO","ASIGNATURA","COORDINADOR","PROGRAMA", "PONDERACION", "DIFERENCIA COORDINADOR","DIFERENCIA PROGRAMA","DIFERENCIA PONDERACION"]
        ws1.append(header)

        for row in file_data:
            ws1.append(row)
            if row[-1] == "modified":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_modified
            elif row[-1] == "not found odoo":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_removed
            elif row[-1] == "not found banner":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_removed

        output = BytesIO()
        wb.save(output)

        self.write({
            'file': base64.b64encode(output.getvalue()),
            'file_name': 'SCADTL_odoo_banner' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx'
        })

        wb.close()
        output.close()
