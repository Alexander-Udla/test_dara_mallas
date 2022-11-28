'''
Created on Mar 18, 2019

@author: fbaez
'''
from odoo import fields, models

class subject_prerequisite_line(models.Model):
    _name="dara_mallas.prerequisite_line"

    period_id=fields.Many2one("dara_mallas.period",'Periodo')
    subject_id=fields.Many2one('dara_mallas.subject','Asignatura')
    subject_code=fields.Char(related="subject_id.code")
    subject_prerequisite_ids = fields.One2many("dara_mallas.prerequisite",inverse_name="prerequisite_line_id",string="Prerrequisitos")

    def copy(self,default=None):
        new_subject_prerequisite_line=super(subject_prerequisite_line,self).copy(default=default)
        prerequisites = []
        for item in self.subject_prerequisite_ids:
            pre = {
                'prerequisite_subject_id':item.prerequisite_subject_id.id,
                'condition':item.condition,
                'conector':item.conector,
                'or_conector':item.or_conector,
                'lparen':item.lparen,
                'test_code':item.test_code,
                'test_score':item.test_score,
                'grade_id':item.grade_id.id,
                'score_id':item.score_id.id,
                'rparen':item.rparen,
                'seq':item.seq,
                'prerequsite_type':item.prerequsite_type,
                'prerequisite_line_id':new_subject_prerequisite_line.id,
            }
            new_prerequisite = self.env['dara_mallas.prerequisite'].create(pre)
            prerequisites.append(new_prerequisite.id)
        new_subject_prerequisite_line.subject_prerequisite_ids=[(6,0,prerequisites)]
        return new_subject_prerequisite_line


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result
class subject_prerequisite(models.Model):
    _name="dara_mallas.prerequisite"
    _order="seq" 

    
    prerequisite_subject_id=fields.Many2one("dara_mallas.subject")
    prerequisite_subject_code=fields.Char("Sigla",related="prerequisite_subject_id.code")
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

    prerequisite_line_id=fields.Many2one("dara_mallas.prerequisite_line")

    def name_get(self):
        result = []
        for rec in self:
            if rec.prerequisite_subject_id:
                result.append((rec.id,'%s - %s' % (str(rec.prerequisite_subject_id.code),str(rec.prerequisite_subject_id.name))))
            elif rec.test_code:
                result.append((rec.id,'%s' % (str(rec.test_code))))
            else:
                pass
        return result

    