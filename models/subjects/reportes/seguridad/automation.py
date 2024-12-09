from venv import logger
from odoo import fields, models, api
from datetime import datetime
from ..repository.automation_repository import automationRepository
import base64
import io
import xlsxwriter
import logging
_logger = logging.getLogger(__name__)


class Equipo:
    def __init__(self,codigo, programa):
        self.codigo = codigo
        self.programa = programa

class Automation(models.Model):
    _name = "dara_mallas.automation"
    _description = "Automatización: notificación de inicio de nuevas cohortes de programas de posgrado."
    
    codigo = fields.Char("CODIGO_PROGRAMA")
    programa = fields.Char("PROGRAMA")
    corte_programa = fields.Char("COHORTE_PROGRAMA")   

    fecha_actual = fields.Date(string="Fecha Actual", default=fields.Date.today, readonly=True)
    
    hello_message = fields.Char(string="Mensaje", default="Hola Mundo")
    
    
    
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
        repository = automationRepository()
        result1 = repository.get_program_postrado('25-NOV-2024')   
        print("result1 ",type(result1))
        print("result1 ",result1)
        
        template = self.env.ref('dara_mallas.file_aproved_mail_template', raise_if_not_found=False)
        if not template:
            _logger.error('No se encontró la plantilla de correo "file_aproved_mail_template".')
            return

        for record in self:
            _logger.info(f"Enviando correo para el registro con ID {record.id}")
            
            # Aquí recorremos los 'line_ids' y mostramos cada uno
            _logger.info(f"Líneas asociadas (line_ids): {record.line_ids}")
            for line in record.line_ids:
                # Mostrar los valores dentro de cada línea
                _logger.info(f"Código: {line.codigo}, Programa: {line.programa}, Cohorte: {line.corte_programa}")
            
            # Mostrar los valores de result1
            _logger.info(f"Valor de result1: {result1}")
            

            # Puedes ver cada elemento de result1 si es una lista o diccionario
            if isinstance(result1, list):
                for res in result1:
                    _logger.info(f"Elemento de result1: {res}")  # Aquí puedes ajustar el formato según la estructura de los datos

            lista =[]
            
            for variable in result1:
                lista.append(Equipo(variable['CODIGO_PROGRAMA'],variable['PROGRAMA']))
                
            context = {
                'object': lista,
                #'hello_message': record.hello_message,
                #'result1': record.result1,
                #'lineIds': record.line_ids
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