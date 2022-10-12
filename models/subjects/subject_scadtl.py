'''
Created on Mar 18, 2019

@author: fbaez
'''
from odoo import fields, models

class subject_scadtl(models.Model):
    _name="dara_mallas.subject_scadtl"
    
    subject_id=fields.Many2one('dara_mallas.subject')
    weighing_id=fields.Many2one('dara_mallas.weighing')
    #coordinador_id
    program_code_id = fields.Many2one('dara_mallas.program_code')
    period_id=fields.Many2one("dara_mallas.period")