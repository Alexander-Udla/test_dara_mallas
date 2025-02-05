'''
Created on 5 jul. 2019

@author: fbaez
'''
from odoo import fields, models

class study_plan_class(models.Model):
    _name="dara_mallas.study_plan_class"
    
    name=fields.Char("Nombre")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )