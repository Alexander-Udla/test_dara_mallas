from odoo import fields, models,api

class subject_no_course(models.Model):
    _name="dara_mallas.subject_no_course" 
    
    subject_attributes_no_course_id = fields.Many2one("dara_mallas.subject_attributes_no_course")
    subject_attributes_code=fields.Char("Sigla", related="subject_attributes_no_course_id.name")

    subject_id=fields.Many2one("dara_mallas.subject")
    study_plan_id=fields.Many2one("dara_mallas.study_plan")
    #no_course_document_id = fields.One2many("dara_mallas.no_course_document",inverse_name="subject_no_course_id")


    
    def name_get(self):
        res = []
        for element in self:
            name = ''
            name += element.subject_attributes_no_course_id.name or ' '
            name += ' - '
            name += element.subject_attributes_no_course_id.description or ''
            name += ' - '
            name += element.subject_id.name or ''
            res.append((element.id, name))
        return res

class subject_attributes_no_course(models.Model):
    _name="dara_mallas.subject_attributes_no_course" 
    
    name = fields.Char("Código")
    description = fields.Char("Descripción")

    
    def name_get(self):
        res = []
        for element in self:
            name = ''
            name += element.description or ' '
           
            res.append((element.id, name))
        return res

class no_course_document(models.Model):
    _name="dara_mallas.no_course_document"

    name = fields.Char("Número de Docto")
    name_dcto = fields.Char("Titulo")
    date_solicitud = fields.Date("Fecha de solicitud")
    date_acept = fields.Date("Fecha de aceptacion")
    subject_no_course_id = fields.Many2one("dara_mallas.subject_no_course")