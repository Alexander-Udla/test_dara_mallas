'''
Created on 17 feb. 2020

@author: udlaec
'''

from odoo import fields, models

class title(models.Model):
    _name='dara_mallas.title'
    
    sniese_code=fields.Char("Codigo SNIESE")
    name=fields.Char('Titulo')
    genre=fields.Selection([('femenino','Femenino'),('masculino','Masculino')],"Genero")
    grade_id=fields.Many2one("dara_mallas.grade")
    
    specialization_id=fields.Many2one("dara_mallas.specialization")
    
    