from odoo import fields, models, api
from datetime import date
from ..repository.automation_repository import automationRepository

class Automation(models.Model):
    _name = "dara_mallas.automation"
    _description = "Automatización: notificación de inicio de nuevas cohortes de programas de posgrado."
    
    codigo = fields.Char("CODIGO_PROGRAMA")
    programa = fields.Char("PROGRAMA")
    corte_programa = fields.Char("COHORTE_PROGRAMA")   

    fecha_actual = fields.Date(string="Fecha Actual", default=fields.Date.today, readonly=True)
    
    line_ids = fields.One2many(
        "dara_mallas.automation.line", 
        "automation_id", 
        string="Programas",
        create=False, 
        edit=False, 
        delete=False,
        readonly=True
    )    
        
    def findProgram(self):
        today = self.fecha_actual
        formatted_date = today.strftime('%d-%b-%Y').upper()        
        
        repository = automationRepository()
        result = repository.get_program_postrado(formatted_date)
        
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
        
class AutomationLine(models.Model):
    _name = "dara_mallas.automation.line"
    _description = "Líneas de Programas"

    codigo = fields.Char("Código")
    programa = fields.Char("Programa")
    corte_programa = fields.Char("Cohorte")
    
    automation_id = fields.Many2one("dara_mallas.automation", string="Automatización")
