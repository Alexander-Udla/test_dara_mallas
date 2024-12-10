from venv import logger
from odoo import fields, models, api
from datetime import date
from ..repository.automation_repository import automationRepository
import base64
import io
import xlsxwriter

class Automation(models.Model):
    _name = "dara_mallas.automation"
    _description = "Automatización: notificación de inicio de nuevas cohortes de programas de posgrado."
    
    codigo = fields.Char("CODIGO_PROGRAMA")
    programa = fields.Char("PROGRAMA")
    corte_programa = fields.Char("COHORTE_PROGRAMA")   
    fecha_actual = fields.Date(string="Fecha Actual", default=fields.Date.today, readonly=True)
    formatted_date = fields.Char(string="Formatted Date", compute='_compute_formatted_date', store=False) 
    
    line_ids = fields.One2many(
        "dara_mallas.automation.line", 
        "automation_id", 
        string="Programas",
        create=False, 
        edit=False, 
        delete=False,
        readonly=True
    )    
    repository = automationRepository()
        
    def findProgram(self):       
        
        
        result = self.repository.get_program_postrado(self.formatted_date)
        print("Programa ",result)
        
        # Limpiar líneas existentes
        self.line_ids = [(5, 0, 0)]
        if result:       
            for record in result:            
                # Crear una línea asociada a este registro
                self.env["dara_mallas.automation.line"].create({
                    'codigo': record.get("CODIGO_PROGRAMA", ""),
                    'programa': record.get("PROGRAMA", ""),
                    'corte_programa': record.get("COHORTE_PROGRAMA", ""),
                    'automation_id': self.id,
                })
        else:            
            self.env["dara_mallas.automation.line"].create({
                'codigo': "Sin información",
                'programa': "Sin información",
                'corte_programa': "Sin información",
                'automation_id': self.id,
            })
    """
    def send_email(self):
        # Obtén la plantilla de correo
        template = self.env.ref('dara_mallas.file_aproved_mail_template', False)
        # Verifica si la plantilla se cargó correctamente
        if not template:
            logger.error('No se encontró la plantilla de correo "file_aproved_mail_template".')
            return
        # Enviar el correo usando la plantilla
        template.send_mail(self.id, force_send=True)
        print("enviado con exito")"""


    def send_email(self):
        # Obtener los datos de result
        result = self.repository.get_program_postrado(self.formatted_date)
        #result1= self.findProgram()  # Suponiendo que la función findProgram retorna 'result'
        print("respuesta ", result)
        # Crear una tabla HTML con los datos de result
        result_html = "<table class='table table-bordered'><thead><tr><th>Código de Programa</th><th>Programa</th><th>Cohorte</th></tr></thead><tbody>"

        for record in result:
            result_html += f"""
            <tr>
                <td>{record.get("CODIGO_PROGRAMA", "")}</td>
                <td>{record.get("PROGRAMA", "")}</td>
                <td>{record.get("COHORTE_PROGRAMA", "")}</td>
            </tr>
            """

        result_html += "</tbody></table>"

        # Crear el cuerpo del correo con la tabla generada
        body_html = f"""
        <h3>Archivo de Graduados Aprobado</h3>
        <div style="font-size: 14px;">
            <p>El archivo adjunto ha sido aprobado para el registro de graduados de</p>
            {result_html}
            <p>DARA</p>
            <p>
                Este es un mensaje enviado automáticamente por el Sistema de Mallas de la 
                Dirección General de Asuntos Regulatorios Académicos desde una cuenta 
                que no es supervisada. Por favor no responda a este correo.
            </p>
        </div>
        """

        # Obtén la plantilla de correo
        template = self.env.ref('dara_mallas.file_aproved_mail_template', False)
        
        # Verifica si la plantilla se cargó correctamente
        if not template:
            logger.error('No se encontró la plantilla de correo "file_aproved_mail_template".')
            return
        
        # Modificar el campo body_html de la plantilla con el nuevo contenido
        template.write({'body_html': body_html})
        
        # Enviar el correo usando la plantilla
        template.send_mail(self.id, force_send=True)
        print("Correo enviado con éxito")

        
        
class AutomationLine(models.Model):
    _name = "dara_mallas.automation.line"
    _description = "Líneas de Programas"
    codigo = fields.Char("Código")
    programa = fields.Char("Programa")
    corte_programa = fields.Char("Cohorte")
    
    automation_id = fields.Many2one("dara_mallas.automation", string="Automatización")