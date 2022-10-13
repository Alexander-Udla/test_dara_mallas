from odoo import models, fields, api
class subject(models.Model):
   
    _name="dara_mallas.subject"

    name=fields.Char("Asignatura, curso o equivalente")
    name_en=fields.Char("Subject, course or equivalent ") 

    short_name=fields.Char("Nombre Corto", size=28)
    code=fields.Char("Sigla", default='ccc-nnnn')
    course_number=fields.Char("Course", size=4, default="nnnn")
    subject_name_id=fields.Many2one("dara_mallas.subject_name")

class subject_rule(models.Model):
    _name="dara_mallas.subject_rule"

    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")
    subject_homologation_ids = fields.One2many("dara_mallas.homologation",inverse_name="subject_rule_id")

class subject_rule_line(models.Model):
    _name="dara_mallas.subject_rule_line"

    subject_rule_id=fields.Many2one("dara_mallas.subject_rule")
    subject_rule_period=fields.Char("Periodo",related="subject_rule_id.period_id.name")

    area_homologation_id=fields.Many2one("dara_mallas.area_homologation") 



class homologation(models.Model):
    _name="dara_mallas.homologation"
    _order="group_id,homologation_subject_id"

    homologation_subject_id=fields.Many2one("dara_mallas.subject",track_visibility='always')
    homologation_subject_code=fields.Char("Sigla",related="homologation_subject_id.code",track_visibility='always')
    subject_rule_rule_id = fields.Many2one("dara_mallas.subject_rule",track_visibility='always')
    subject_rule_id = fields.Many2one("dara_mallas.subject_rule",track_visibility='always')
    subject_attributes_id = fields.Many2one("dara_mallas.subject_attributes")
    group_id=fields.Many2one("dara_mallas.group_rule",track_visibility='always') 
    condition=fields.Char("Condiciones",track_visibility='always')
    test=fields.Char("Prueba",track_visibility='always')
    min_score=fields.Integer("Puntaje Minimo",track_visibility='always')
    max_score=fields.Integer("Puntaje maximo",track_visibility='always')
    rule_min_score_id=fields.Many2one('dara_mallas.rule_score', string="Calificacion minima")

class group_rule(models.Model):
    _name="dara_mallas.group_rule"
    
    name=fields.Char("Agrupador")

class rule_score(models.Model):
    _name="dara_mallas.rule_score"
    
    name=fields.Char("Calificacion")  


class elective_line(models.Model):
    _name="dara_mallas.elective_line"
     
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")

    elective_ids=fields.One2many("dara_mallas.elective",inverse_name="elective_line_id")

class elective(models.Model):
    _name="dara_mallas.elective"
   
    elective_subject_id=fields.Many2one("dara_mallas.subject")
    elective_subject_code=fields.Char("Sigla",related="elective_subject_id.code")

    elective_line_id=fields.Many2one("dara_mallas.elective_line")


class itinerary_line(models.Model):
    _name="dara_mallas.itinerary_line"
     
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one("dara_mallas.subject")

    itinerary_ids=fields.One2many("dara_mallas.itinerary",inverse_name="itinerary_line_id")

class itinerary(models.Model):
    _name="dara_mallas.itinerary"

   
    itinerary_subject_id=fields.Many2one("dara_mallas.subject")
    itinerary_subject_code=fields.Char("Sigla",related="itinerary_subject_id.code")
    specialization_id=fields.Many2one("dara_mallas.specialization")

    itinerary_line_id=fields.Many2one("dara_mallas.itinerary_line")