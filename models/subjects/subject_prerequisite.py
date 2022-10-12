'''
Created on Mar 18, 2019

@author: fbaez
'''
from odoo import fields, models

class subject_prerequisite_line(models.Model):
    _name="dara_mallas.subject_prerequisite_line"

    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one('dara_mallas.subject')
    subject_prerequisite_ids = fields.One2many("dara_mallas.prerequisite",inverse_name="subject_prerequisite_line_id")

class subject_prerequisite(models.Model):
    _name="dara_mallas.prerequisite"
    _order="seq" 

    
    prerequisite_subject_id=fields.Many2one("dara_mallas.subject")
    prerequisite_subject_code=fields.Char("Sigla",related="prerequisite_subject_id.code")
    group_id=fields.Many2one("dara_mallas.group_rule")
    condition=fields.Char("Condiciones")
    conector=fields.Selection([('Y','Y'),('O','O')],"Conector")
    or_conector=fields.Boolean("O")
    lparen=fields.Char("(")
    test_code=fields.Char("Codigo Examen")
    test_score=fields.Float("Puntaje Examen")
    grade_id=fields.Many2one("dara_mallas.grade")
    score_id=fields.Many2one('dara_mallas.rule_score', string="Calificacion")
    rparen=fields.Char(")")
    seq = fields.Integer("Seq")
    prerequsite_type=fields.Selection([('malla','Malla'),('homologacion','Homologacion')],"Tipo",default='malla')

    subject_prerequisite_line_id=fields.Many2one("dara_mallas.subject_prerequisite_line")

    