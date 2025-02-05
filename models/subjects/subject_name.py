'''
Created on Apr 12, 2019

@author: fbaez
'''

from odoo import fields,models

class subject_name(models.Model):
    _name="dara_mallas.subject_name"
    
    name=fields.Char("Nombre")
    code=fields.Char("Codigo")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )