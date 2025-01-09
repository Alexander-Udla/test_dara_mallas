from odoo import models, api, fields

class coordinator(models.Model):
    _name="dara_mallas.coordinator"
    
    name=fields.Char("Nombres")
    idbanner=fields.Char("ID Banner")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
