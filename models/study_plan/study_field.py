'''
Created on Mar 13, 2019

@author: fbaez
'''
from odoo import models, fields

class study_field(models.Model):
    _name="dara_mallas.study_field"
    
    name=fields.Char("Campo de formacion")
    number=fields.Integer("Número")
    color=fields.Char("Color")
    font_color=fields.Char("Color",default="#000000")
    