from venv import logger
from odoo import fields, models, api
from datetime import date
from ..repository.automation_repository import automationRepository
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class Automation(models.TransientModel):
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
    
        
    
    @api.depends('fecha_actual')
    def _compute_formatted_date(self):
        for record in self:
            if record.fecha_actual:
                record.formatted_date = record.fecha_actual.strftime('%d-%b-%Y').upper()
            else:
                record.formatted_date = ""


    def send_email(self):      
        formatted_date = datetime.now().strftime('%d-%b-%Y').upper()        
        repository = automationRepository(self.env)
        result = repository.get_number_student(formatted_date)
        
        if not result:  # Si no hay datos, salir de la función
            _logger.info(f"No hay información disponible para el día {formatted_date}. No se enviará correo.")
            return
        
        keys = ["CODIGO_PROGRAMA", "PROGRAMA", "COHORTE_PROGRAMA", "NUMERO_ESTUDIANTES"]
        result = [dict(zip(keys, row)) for row in result]
        
        for resp in result:
            codigo_programa = resp.get("CODIGO_PROGRAMA", "")
            if codigo_programa:  # Asegurarse de que no esté vacío
                find = repository.get_number_cohorte(codigo_programa)
            
                cohorte_programa = resp.get("COHORTE_PROGRAMA", "")
                if find:
                    keys = ["GORSDAV_PK_PARENTTAB", "POSICION"]
                    find_dicts = [dict(zip(keys, cohorte)) for cohorte in find]
                    for cohorte in find_dicts:
                        if cohorte.get("GORSDAV_PK_PARENTTAB") == cohorte_programa:                            
                            resp["COHORTE"] = cohorte.get("POSICION")
                            break 
                    
                 
        result_html = """
            <table class='table table-bordered'>
                <thead>
                    <tr>
                        <th>Código de Programa</th>
                        <th>Programa</th>
                        <th>Cohorte</th>
                        <th> # Estudiantes</th>
                        <th> # Cohorte</th>
                    </tr>
                </thead>
                <tbody>
            """
        for record in result:
            result_html += f"""
            <tr>
                <td style="text-align: center;">{record.get("CODIGO_PROGRAMA", "")}</td>
                <td style="text-align: center;">{record.get("PROGRAMA", "")}</td>
                <td style="text-align: center;">{record.get("COHORTE_PROGRAMA", "")}</td>
                <td style="text-align: center;">{record.get("NUMERO_ESTUDIANTES", "")}</td>
                <td style="text-align: center;">{record.get("COHORTE", "")}</td>
            </tr>
            """
        result_html += "</tbody></table>"

        body_html = f"""
        <h3>NOTIFICACION: PROGRAMAS DE POSTGRADO QUE INICIAN ACTIVIDADES HOY {formatted_date}</h3>
        <div style="font-size: 14px;">            
            {result_html}
            
            <p>
                Este es un mensaje enviado automáticamente por el Sistema de Mallas de la 
                Dirección General de Asuntos Regulatorios Académicos. Por favor no responda a este correo.
            </p>
        </div>
            """

        template = self.env.ref('dara_mallas.file_aproved_mail_template', False)
        
        
        if not template:
            logger.error('No se encontró la plantilla de correo "file_aproved_mail_template".')
            return
        
        template.write({'body_html': body_html})
        template.send_mail(self.id, force_send=True)

               
class AutomationLine(models.TransientModel):
    _name = "dara_mallas.automation.line"
    _description = "Correo de cohorte config"
    codigo = fields.Char("Código")
    programa = fields.Char("Programa")
    corte_programa = fields.Char("Cohorte")
    
    automation_id = fields.Many2one("dara_mallas.automation", string="Automatización")