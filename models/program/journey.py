'''
Created on Mar 18, 2019

@author: fbaez
'''

from odoo import fields, models

class journey(models.Model):
    _name="dara_mallas.journey"
    
    name=fields.Char("Jornada")
    code=fields.Char("Codigo")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )