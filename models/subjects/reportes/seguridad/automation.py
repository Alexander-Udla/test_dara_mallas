from venv import logger
from odoo import fields, models, api
from datetime import datetime
from ..repository.automation_repository import automationRepository
import base64
import io
import xlsxwriter
import logging
_logger = logging.getLogger(__name__)


class Automation(models.Model):
    _name = "dara_mallas.automation"
    _description = "Automatización: notificación de inicio de nuevas cohortes de programas de posgrado."
    
    codigo = fields.Char("CODIGO_PROGRAMA")
    programa = fields.Char("PROGRAMA")
    corte_programa = fields.Char("COHORTE_PROGRAMA")   

    fecha_actual = fields.Date(string="Fecha Actual", default=fields.Date.today, readonly=True)
    
    hello_message = fields.Char(string="Mensaje", default="Hola Mundo")
    repository = automationRepository()
    result1 = repository.get_program_postrado(fecha_actual)   
    print("result1 ",type(result1))
      
    
    
    line_ids = fields.One2many(
        "dara_mallas.automation.line", 
        "automation_id", 
        string="Programas",        
        readonly=True
    )    
        
    def findProgram(self):
        today = self.fecha_actual
        formatted_date = today.strftime('%d-%b-%Y').upper()        
        
        #repository = automationRepository()
        result = self.repository.get_program_postrado(formatted_date)

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
            
    def send_email(self):
        template = self.env.ref('dara_mallas.file_aproved_mail_template', raise_if_not_found=False)
        print("Cuerpo ", self.line_ids)
        if not template:
            _logger.error('No se encontró la plantilla de correo "file_aproved_mail_template".')
            return

        for record in self:
            _logger.info(f"Enviando correo para el registro con ID {record.id}")
            context = {
                'object': record,
                'hello_message': record.hello_message,  # Pasamos la variable 'hello_message' a la plantilla
                'result1':record.line_ids
            }

            # Enviar el correo con el contexto
            template.with_context(context).send_mail(record.id, force_send=True)


    
                
    
    """
    def send_email(self):
        print("ingreso")
        template = self.env.ref('dara_mallas.file_aproved_mail_template', raise_if_not_found=False)

        # Verifica si la plantilla se cargó correctamente
        if not template:
            _logger.error('No se encontró la plantilla de correo "file_aproved_mail_template".')
            return
        print("Self ", self)
        for record in self:
            print("record ",record)
            print("recordline_ids ",record.line_ids)
            if not record.line_ids:
                _logger.warning(f"El registro con ID {record.id} no tiene líneas asociadas para enviar en el correo.")
                continue
            
            # Enviar el correo
            template.send_mail(record.id, force_send=True)
            print(f"Correo enviado con éxito para el registro con ID {record.id}")

        #template.send_mail(self.id, force_send=True)
        #print("enviado con exito")
      """

            
        
        
        
class AutomationLine(models.Model):
    _name = "dara_mallas.automation.line"
    _description = "Líneas de Programas"

    codigo = fields.Char("Código")
    programa = fields.Char("Programa")
    corte_programa = fields.Char("Cohorte")
    
    automation_id = fields.Many2one("dara_mallas.automation", string="Automatización")