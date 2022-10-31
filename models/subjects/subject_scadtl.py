'''
Created on Mar 18, 2019

@author: fbaez
'''
from odoo import fields, models

class subject_scadtl(models.Model):
    _name="dara_mallas.subject_scadtl"
    
    subject_id=fields.Many2one('dara_mallas.subject')
    weighing_id=fields.Many2one('dara_mallas.weighing')
    coordinador_id = fields.Many2one('dara_mallas.coordinator','Coordinador')
    program_code_id = fields.Many2one('dara_mallas.program_code')
    period_id=fields.Many2one("dara_mallas.period")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result