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
    sniese_title_ids=fields.One2many("dara_mallas.title", inverse_name="specialization_id")
    saes_speciality_plan_code=fields.Char("Codigo especializacion + plan SAES")
class specialization_major(models.Model):
    _name="dara_mallas.specialization_major"
    
    name=fields.Char("Major")
    number=fields.Integer("Numero")
    code=fields.Char("codigo / numero")

    specialization_id=fields.Many2one("dara_mallas.specialization")
    saes_code_id=fields.Many2one("dara_mallas.saes_code")
    


       
    
