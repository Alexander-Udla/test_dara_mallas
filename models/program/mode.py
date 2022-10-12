'''
Created on Mar 13, 2019

@author: fbaez
'''
from odoo import models, fields

class mode(models.Model):
    _name="dara_mallas.mode"
    
    name=fields.Char("Modalidad")
    code=fields.Char("codigo")