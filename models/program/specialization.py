'''
Created on Mar 13, 2019

@author: fbaez
'''



from odoo import models, fields,api
from odoo.exceptions import UserError

        
class specializations(models.Model):
    _name='dara_mallas.specialization'
     
    name=fields.Char("Especialización")
    color=fields.Char("Color")
    major_ids=fields.One2many("dara_mallas.specialization_major", inverse_name="specialization_id")
    program_id=fields.Many2one("dara_mallas.program")
 
class specialization_major(models.Model):
    _name="dara_mallas.specialization_major"
    
    name=fields.Char("Major")
    number=fields.Integer("Numero")
    code=fields.Char("codigo / numero")

    specialization_id=fields.Many2one("dara_mallas.specialization")
    


       
    
