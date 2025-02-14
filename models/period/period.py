from odoo import models, fields, api
class period(models.Model):
   
    _name="dara_mallas.period"
     
    name = fields.Char("Periodo academico")
    description = fields.Char("Descripción")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )