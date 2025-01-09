from odoo import fields, models

    
class resolutions(models.Model):
    _name='dara_mallas.resolutions'
    name = fields.Char('Resolución')
    date = fields.Date('Fecha resolución')
    file=fields.Binary("Archivo")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
    
    