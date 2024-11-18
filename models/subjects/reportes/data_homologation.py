import xlsxwriter # type: ignore
import psycopg2 # type: ignore
import base64
from odoo import fields, models, api # type: ignore
from odoo.exceptions import UserError # type: ignore
from io import BytesIO
from reportlab.pdfgen import canvas


class DataHomologation(models.Model):
    _name = "dara_mallas.data_homologations"
    _description = "Conexión a base de datos y generación de PDF"

    status = fields.Selection(selection=[("pruebas", "Pruebas"), ("produccion", "Producción")], string="Estado")
    period = fields.Many2one('dara_mallas.period', string="Periodo", domain=[])
    pdf_file = fields.Binary("Archivo PDF")    
    excel_file = fields.Binary("Archivo Excel")
    
    pdf_file_name = fields.Char("Nombre del Archivo PDF")
    excel_file_name = fields.Char("Nombre del Archivo Excel")
    
    @api.onchange('status')
    def _onchange_status(self):
        self.period = False
        if not self.status:
            return {
                'domain': {'period': [('id', '=', False)]}
            }
        
        db_name = 'mallas-prueba' if self.status == 'pruebas' else 'mallas'

        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user="alex",
                password="root123",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM dara_mallas_period;")
            result = cur.fetchall()
            cur.close()
            conn.close()

            if not result:
                raise UserError("No se encontraron periodos en la base de datos.")

            period_ids = [p[0] for p in result]
            existing_periods = self.env['dara_mallas.period'].search([('id', 'in', period_ids)])
            new_periods = [p for p in result if p[0] not in existing_periods.ids]
            for period in new_periods:
                self.env['dara_mallas.period'].create({'id': period[0], 'name': period[1]})

            return {
                'domain': {'period': [('id', 'in', period_ids)]}
            }

        except Exception as e:
            raise UserError(f"No se pudo conectar a la base de datos {db_name}: {str(e)}")

    
    def generate_pdf(self):
        if not self.period:
            raise UserError("Por favor, seleccione un periodo para generar el PDF.")
        return self.env.ref('dara_mallas.data_homologation_report_action').report_action(self) 
    
   
   
   
    
    def generate_excel(self):
        if not self.period:
            raise UserError("Por favor, seleccione un periodo para generar el archivo Excel.")

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        sheet = workbook.add_worksheet("Homologación")
        
        format1 = workbook.add_format({'font_size': 13, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 13, 'align': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1})
        
        
        # Escribir encabezados
        headers = ["Estado", "Periodo", "Descripción de Prueba"]
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Escribir datos
        sheet.write(1, 0, dict(self._fields['status'].selection).get(self.status), format1)
        sheet.write(1, 1, self.period.name or "Sin Definir", format2)        
        
        workbook.close()
        output.seek(0)

        encoded_excel = base64.b64encode(output.read())

        # Imprimir el contenido base64 en consola para verificar
        print(f"Excel generado (base64): {encoded_excel[:100]}...")  # Imprime los primeros 100 caracteres del base64

        self.write({
            'excel_file': encoded_excel,
            'excel_file_name': "Homologacion_{}.xlsx".format(self.period)
        })

        output.close()

        # Retornar acción de descarga directa
        return {
            'type': 'ir.actions.act_url',
            'url': f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{self.excel_file.decode()}',
            'target': 'self',
            'download': self.excel_file_name,
        }
