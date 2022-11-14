from odoo import models, fields, api

class schedule_class(models.Model):
    _name="dara_mallas.schedule_class"
    
    name=fields.Char("Descripcion")
    code=fields.Char("Codigo")

class schedule_class_line(models.Model):
    _name="dara_mallas.schedule_class_line"
    
    schedule_class_id=fields.Many2one("dara_mallas.schedule_class")
    schedule_class_code=fields.Char("Codigo", related="schedule_class_id.code")
    default=fields.Boolean("Default")
    
    schedule_class_line_subject_id=fields.Many2one("dara_mallas.schedule_class_line_subject")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.schedule_class_code))))
        return result

class schedule_class_line_subject(models.Model):
    _name="dara_mallas.schedule_class_line_subject"
    
    period_id=fields.Many2one("dara_mallas.period")
    subject_id=fields.Many2one('dara_mallas.subject')
    subject_code=fields.Char(related="subject_id.code")
    schedule_class_line_ids =fields.One2many("dara_mallas.schedule_class_line",inverse_name="schedule_class_line_subject_id")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s / %s' % (str(rec.subject_id.code),str(rec.subject_id.name),str(rec.period_id.name))))
        return result