'''
Created on 6 jun. 2019

@author: fbaez
'''
from odoo import fields, models

class subject_department(models.Model):
    _name="dara_mallas.subject_department"
    
    code = fields.Char("Codigo")
    name=fields.Char("Nombre")
    college_id=fields.Many2one("dara_mallas.college")
    
    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )