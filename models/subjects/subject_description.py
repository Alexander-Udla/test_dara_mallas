from odoo import models, fields, api
class subject_description(models.Model):
    _name="dara_mallas.subject_description_line"

    subject_id=fields.Many2one("dara_mallas.subject")
    subject_code=fields.Char(related="subject_id.code")
    subject_name_en=fields.Char(related="subject_id.name_en")
    content_description=fields.Text("Descripcion mínima",track_visibility='always')
    content_description_en=fields.Text("Minimum description",track_visibility='always')
    period_id=fields.Many2one("dara_mallas.period","Periodo")
    tipo = fields.Char("Tipo")
    state=fields.Selection([('revisado','Revisado'),('por revisar','Por Revisar')], string="Estado")

    company_id = fields.Many2one(
        'res.company',
        string = 'Empresa',
        default=lambda self: self.env.company,
        help = 'La empresa pertenece a este registro'
    )
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,'%s - %s' % (str(rec.subject_id.name),str(rec.subject_id.code))))
        return result



    