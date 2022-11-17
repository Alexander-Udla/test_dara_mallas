'''
Created on Mar 14, 2019

@author: fbaez
'''
from odoo import fields, models

class subject_class(models.Model): 
    _name="dara_mallas.subject_class_name"
    
    name=fields.Char("Clase de asignatura") 

class subject_class_line(models.Model):
    _name="dara_mallas.subject_class"
    
    subject_class_id=fields.Many2one("dara_mallas.subject_class_name",string="Clase de Sigla") 
    subject_id=fields.Many2one("dara_mallas.subject") 

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.subject_class_id.name))))
        return result