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

class grade_line(models.Model):
    _name='dara_mallas.grade_line'

    grade_id=fields.Many2one("dara_mallas.grade")
    grade_description=fields.Char("Descripción",related="grade_id.description")
    grade_line_subject_id=fields.Many2one("dara_mallas.grade_line_subject")
class grade_line_subject(models.Model):
    _name='dara_mallas.grade_line_subject'
    
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one('dara_mallas.subject')
    grade_line_ids=fields.One2many("dara_mallas.grade_line",inverse_name="grade_line_subject_id")
#===============================================================================
# El siguiente modelo contiene  el modo de calificacion 
# S. Standard  
# A. Aprueba Reprueba
# T. Transfer??
#===============================================================================
class grade_mode(models.Model):
    _name="dara_mallas.grade_mode"
    
    name=fields.Char("Modo Calificacion")
    description=fields.Char("Descripcion") 
    grade_mode_line_subject_id=fields.Many2one("dara_mallas.grade_mode_line_subject")
class grade_mode_line(models.Model):
    _name="dara_mallas.grade_mode_line"
    
    grade_mode_id=fields.Many2one("dara_mallas.grade_mode")
    grade_mode_description=fields.Char("Descripción",related="grade_mode_id.description")
    grade_mode_line_subject_id=fields.Many2one("dara_mallas.grade_mode_line_subject")

class grade_mode_line_subject(models.Model):
    _name='dara_mallas.grade_mode_line_subject'
    
    grade_mode_line_ids=fields.One2many("dara_mallas.grade_mode_line",inverse_name="grade_mode_line_subject_id")
    subject_id=fields.Many2one('dara_mallas.subject')
    period_id=fields.Many2one("dara_mallas.period")

class subject_status(models.Model):
    _name="dara_mallas.subject_status"
    
    name=fields.Char("Status")
    description=fields.Char("Descripcion")




    

