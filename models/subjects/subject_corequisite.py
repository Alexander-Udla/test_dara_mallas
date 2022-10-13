'''
Created on Apr 12, 2019

@author: fbaez
'''

from odoo import fields,models

class corequisite(models.Model):
    _name="dara_mallas.corequisite"
    
    corequisite_subject_id=fields.Many2one("dara_mallas.subject")
    corequisite_subject_code=fields.Char("Sigla",related="corequisite_subject_id.code")

    corequisite_line_id=fields.Many2one("dara_mallas.corequisite_line")
class corequisite_line(models.Model):
    _name="dara_mallas.corequisite_line"
    
    period_id=fields.Many2one("dara_mallas.period") 
    subject_id=fields.Many2one("dara_mallas.subject")
    corequisite_ids=fields.One2many("dara_mallas.corequisite",inverse_name="corequisite_line_id")

