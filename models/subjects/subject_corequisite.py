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

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.corequisite_subject_id.code),str(rec.corequisite_subject_id.name))))
        return result
class corequisite_line(models.Model):
    _name="dara_mallas.corequisite_line"
    
    period_id=fields.Many2one("dara_mallas.period",'Periodo') 
    subject_id=fields.Many2one("dara_mallas.subject",'Asignatura')
    subject_code=fields.Char(related="subject_id.code")
    corequisite_ids=fields.One2many("dara_mallas.corequisite",inverse_name="corequisite_line_id",string="Correquisitos")


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result

