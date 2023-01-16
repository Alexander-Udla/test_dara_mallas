from odoo import models, fields, api
class subject_description_line(models.Model):
    _name="dara_mallas.subject_description_line"

    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char(related="subject_id.code")
    subject_description_ids = fields.One2many("dara_mallas.subject_description",inverse_name="subject_description_id",string="Sílabos")
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_id.name),str(rec.subject_id.code))))
        return result

class subject_description(models.Model):
    _name="dara_mallas.subject_description"

    period_id=fields.Many2one("dara_mallas.period")
    content_description=fields.Text("Descripcion mínima",track_visibility='always')
    content_description_en=fields.Text("Minimum description",track_visibility='always')
    state = fields.Boolean("Estado", default=True,track_visibility='always')

    subject_description_id = fields.Many2one("dara_mallas.subject_description")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s' % (str(rec.period_id.name))))
        return result


    