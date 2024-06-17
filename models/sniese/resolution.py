from odoo import fields, models

    
class resolutions(models.Model):
    _name='dara_mallas.resolutions'
    name = fields.Char('Resolución')
    date = fields.Date('Fecha resolución')
    file=fields.Binary("Archivo")
    
    