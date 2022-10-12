'''
Created on 17 feb. 2020

@author: udlaec
'''
from odoo import fields, models


#===============================================================================
# este modelo almacena informacion del nivel de studio 
# UG para pregrado
# GR para posgrado
#===============================================================================
class grade(models.Model):
    _name='dara_mallas.grade'
    
    name=fields.Char("Nivel")
    description=fields.Char("Descripcion") 

class grade_line_subject(models.Model):
    _name='dara_mallas.grade_line_subject'
    
    grade_id=fields.Many2one("dara_mallas.grade")
    grade_code=fields.Char('Codigo',related='grade_id.description')
    subject_id=fields.Many2one('dara_mallas.subject')
    period_id=fields.Many2one("dara_mallas.period")

#===============================================================================
# El siguiente modelo contiene  el modo de calificacion 
# S. Standard  
# A. Aprueba Reprueba
# T. Transfer??
#===============================================================================
class grade_mode(models.Model):
    _name="udla_mallas_grade_mode"
    
    name=fields.Char("Modo Calificacion")
    description=fields.Char("Descripcion") 

class grade_mode_line_subject(models.Model):
    _name='dara_mallas.grade_mode_line_subject'
    
    grade_mode_id=fields.Many2one("udla_mallas_grade_mode")
    grade_mode_code=fields.Char('Codigo',related='grade_mode_id.description')
    subject_id=fields.Many2one('dara_mallas.subject')
    period_id=fields.Many2one("dara_mallas.period")

class subject_status(models.Model):
    _name="dara_mallas.subject_status"
    
    name=fields.Char("Status")
    description=fields.Char("Descripcion")




    

