from odoo import models, fields, api
class period(models.Model):
   
    _name="dara_mallas.period"
     
    name = fields.Char("Periodo academico")
    description = fields.Char("Descripción")