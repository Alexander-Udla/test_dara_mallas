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

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

class grade_line(models.Model):
    _name='dara_mallas.grade_line'

    grade_id=fields.Many2one("dara_mallas.grade")
    grade_description=fields.Char("Descripción",related="grade_id.description")
    grade_line_subject_id=fields.Many2one("dara_mallas.grade_line_subject")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.grade_id.name))))
        return result
class grade_line_subject(models.Model):
    _name='dara_mallas.grade_line_subject'
    
    period_id=fields.Many2one("dara_mallas.period",'Periodo')
    subject_id=fields.Many2one('dara_mallas.subject','Asignatura')
    subject_code=fields.Char(related="subject_id.code")
    grade_line_ids=fields.One2many("dara_mallas.grade_line",inverse_name="grade_line_subject_id",string="Nivel")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_id.code),str(rec.subject_id.name))))
        return result
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

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

class grade_mode_line(models.Model):
    _name="dara_mallas.grade_mode_line"
    
    grade_mode_id=fields.Many2one("dara_mallas.grade_mode")
    grade_mode_description=fields.Char("Descripción",related="grade_mode_id.description")
    grade_mode_line_subject_id=fields.Many2one("dara_mallas.grade_mode_line_subject")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.grade_mode_id.name))))
        return result

class grade_mode_line_subject(models.Model):
    _name='dara_mallas.grade_mode_line_subject'
    
    grade_mode_line_ids=fields.One2many("dara_mallas.grade_mode_line",inverse_name="grade_mode_line_subject_id",string="Tipo Calificación")
    subject_id=fields.Many2one('dara_mallas.subject','Asignatura')
    subject_code=fields.Char(related="subject_id.code")
    period_id=fields.Many2one("dara_mallas.period",'Periodo')

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_id.code),str(rec.subject_id.name))))
        return result

class subject_status(models.Model):
    _name="dara_mallas.subject_status"
    
    name=fields.Char("Status")
    description=fields.Char("Descripcion")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

class banner_grade(models.Model):
    _name="dara_mallas.banner_grade"
    
    code=fields.Char("Code") 
    name=fields.Char("Descripcion")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )

#=======MODALIDAD DE TITULACIÓN===============================

class graduation_mode(models.Model):
    _name="dara_mallas.graduation_mode"
    
    graduation_mode_id = fields.Many2one("dara_mallas.graduation_mode_data")
    study_plan_id=fields.Many2one("dara_mallas.study_plan")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
    
class graduation_mode_data(models.Model):
    _name="dara_mallas.graduation_mode_data"
    
    name=fields.Char("Modalidad de titulacion")
    codigo=fields.Char("Código")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )




    

