'''
Created on Apr 12, 2019

@author: fbaez
'''

from odoo import fields,models

class subject_corequisite(models.Model):
    _name="dara_mallas.subject_corequisite"
    
    period_id=fields.Many2one("dara_mallas.period") 
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char("Sigla", related="subject_id.code")
    corequisite_subject_id=fields.Many2one("dara_mallas.subject")
    corequisite_subject_code=fields.Char("Sigla",related="corequisite_subject_id.code")