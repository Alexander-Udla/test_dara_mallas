'''
Created on Mar 14, 2019

@author: fbaez
'''
from odoo import fields, models

class subject_class(models.Model):
    _name="dara_mallas.subject_class"
    
    name=fields.Char("Clase de asignatura")

class subject_class_line(models.Model):
    _name="dara_mallas.subject_class"
    
    period_id=fields.Many2one("dara_mallas.period") 
    subject_id=fields.Many2one("dara_mallas.subject") 
    subject_class_id=fields.Many2one("dara_mallas.subject_class") 

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.subject_class_id.name))))
        return result