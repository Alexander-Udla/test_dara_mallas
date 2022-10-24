'''
Created on Mar 13, 2019

@author: fbaez
'''
from odoo import models, fields

class organization_unit(models.Model):
    _name="dara_mallas.organization_unit"
    
    name=fields.Char("Unidad de organizacion")
    color=fields.Char("Color")